#!/usr/bin/env python3
"""video-eyes: turn a short video into something an AI agent can actually "watch".

Given a local video file (a Reel, TikTok or Short you saved), it writes:

  <out>/timeline.json     shots with start/end times, cut rate, hook-window stats, audio
                          profile, transcript (with timings when available), file list
  <out>/frames/           one JPEG per shot + dense frames across the first 3 seconds
  <out>/contact-sheet.jpg every frame in one image, left-to-right, top-to-bottom, in the
                          order listed in timeline.json "contact_sheet_order"

The agent then reads timeline.json and looks at the frames (any multimodal model can read
JPEGs), so it sees the hook, the cuts and the on-screen text instead of guessing.

Requirements: Python 3.8+ (standard library only) and ffmpeg + ffprobe on PATH.
Optional, used automatically when present:
  - transcription: the `faster_whisper` Python package, or the `whisper` CLI (openai-whisper),
    or the `whisper-cli` binary from whisper.cpp (set WHISPER_CPP_MODEL to a ggml model path)
  - a sidecar subtitle file next to the video (same name, .vtt or .srt), used before whisper
  - `tesseract` for an OCR hint per frame (the agent should still read the frames itself)
  - `yt-dlp`, only when you pass a URL instead of a file (TikTok and YouTube work without a
    login; Instagram usually needs a logged-in session, so save the Reel with Instagram's own
    Share > Download instead)

Nothing here calls a paid service or needs an account or API key.

Usage:
  python3 video-eyes.py path/to/reel.mp4 [--out DIR] [--scene 0.30] [--no-transcript]
  python3 video-eyes.py https://www.tiktok.com/@user/video/123 --out remake/
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HOOK_WINDOW = 3.0          # seconds that decide whether people keep watching
HOOK_FRAME_STEP = 0.5      # dense sampling inside the hook window
MAX_SHOT_GAP = 4.0         # no cut for this long -> sample a frame anyway (static shots)
FRAME_WIDTH = 540          # enough to read on-screen text, small enough for context windows


def run(cmd, check=True):
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def need(binary):
    if shutil.which(binary) is None:
        sys.exit(f"video-eyes: '{binary}' not found on PATH. Install ffmpeg "
                 f"(macOS: brew install ffmpeg, Debian/Ubuntu: apt install ffmpeg), "
                 f"or fall back to screenshots (see the skill's capability levels).")


def fetch_url(url, workdir):
    if shutil.which("yt-dlp") is None:
        sys.exit("video-eyes: got a URL but yt-dlp isn't installed. Save the video file "
                 "instead (Instagram: Share > Download) and pass its path.")
    if "instagram.com" in url:
        print("video-eyes: note: Instagram usually blocks downloads without a logged-in "
              "session. If this fails, use Instagram's Share > Download and pass the file.",
              file=sys.stderr)
    tpl = os.path.join(workdir, "source.%(ext)s")
    res = run(["yt-dlp", "-f", "mp4/best", "--write-auto-subs", "--sub-format", "vtt",
               "--write-info-json", "-o", tpl, url], check=False)
    if res.returncode != 0:
        sys.exit("video-eyes: yt-dlp could not fetch that URL:\n" + res.stderr[-800:])
    vids = [f for f in os.listdir(workdir) if f.startswith("source.") and
            f.rsplit(".", 1)[-1] in ("mp4", "webm", "mkv", "mov")]
    if not vids:
        sys.exit("video-eyes: yt-dlp finished but no video file was written.")
    return os.path.join(workdir, vids[0])


def probe(path):
    res = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format",
               "-show_streams", path])
    data = json.loads(res.stdout)
    v = next((s for s in data["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    if v is None:
        sys.exit("video-eyes: no video stream found in that file.")
    num, _, den = (v.get("avg_frame_rate") or "0/1").partition("/")
    fps = round(float(num) / float(den), 2) if den and float(den) else None
    w, h = int(v.get("width", 0)), int(v.get("height", 0))
    rotate = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rotate = abs(int(sd["rotation"])) % 360
    if rotate in (90, 270):
        w, h = h, w
    return {
        "duration_s": round(float(data["format"].get("duration", 0)), 2),
        "width": w, "height": h, "fps": fps,
        "aspect": f"{w}:{h}" if not (w and h) else _aspect(w, h),
        "has_audio": a is not None,
    }


def _aspect(w, h):
    r = w / h
    for name, val in (("9:16", 9 / 16), ("4:5", 4 / 5), ("1:1", 1.0), ("16:9", 16 / 9)):
        if abs(r - val) < 0.03:
            return name
    return f"{w}:{h}"


def detect_cuts(path, threshold):
    res = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an", "-vf",
               f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"], check=False)
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", res.stderr)]
    return sorted(t for t in times if t > 0.2)


def build_shots(cuts, duration):
    bounds = [0.0] + [c for c in cuts if c < duration - 0.1] + [duration]
    shots = []
    for i in range(len(bounds) - 1):
        start, end = bounds[i], bounds[i + 1]
        if end - start < 0.15:      # flash frames: merge into the previous shot
            if shots:
                shots[-1]["end"] = round(end, 2)
            continue
        shots.append({"start": round(start, 2), "end": round(end, 2)})
    for i, s in enumerate(shots, 1):
        s["shot"] = i
        s["length_s"] = round(s["end"] - s["start"], 2)
    return shots


def sample_times(shots):
    """One frame per shot (just after the cut), extra frames for long static shots,
    and dense frames across the hook window."""
    picks = {}
    for s in shots:
        t = min(s["start"] + 0.3, (s["start"] + s["end"]) / 2)
        picks[round(t, 2)] = f"shot {s['shot']}"
        t2 = s["start"] + MAX_SHOT_GAP
        while t2 < s["end"] - 0.5:
            picks.setdefault(round(t2, 2), f"shot {s['shot']} (held)")
            t2 += MAX_SHOT_GAP
    t = 0.0
    end = min(HOOK_WINDOW, shots[-1]["end"] - 0.05) if shots else 0
    while t <= end:
        picks.setdefault(round(t, 2), "hook window")
        t += HOOK_FRAME_STEP
    return sorted(picks.items())


def extract_frames(path, times, frames_dir):
    os.makedirs(frames_dir, exist_ok=True)
    out = []
    for i, (t, why) in enumerate(times, 1):
        name = f"f{i:03d}_{t:06.2f}s.jpg"
        dest = os.path.join(frames_dir, name)
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t}", "-i", path,
             "-frames:v", "1", "-vf", f"scale={FRAME_WIDTH}:-2", "-q:v", "3", dest], check=False)
        if os.path.exists(dest):
            out.append({"t": t, "file": f"frames/{name}", "why": why})
    return out


def contact_sheet(frames, out_dir):
    if not frames:
        return None
    cols = 4 if len(frames) > 6 else min(3, len(frames))
    rows = -(-len(frames) // cols)
    with tempfile.TemporaryDirectory() as tmp:
        for i, f in enumerate(frames):
            os.symlink(os.path.abspath(os.path.join(out_dir, f["file"])),
                       os.path.join(tmp, f"{i:04d}.jpg"))
        dest = os.path.join(out_dir, "contact-sheet.jpg")
        res = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", "1",
                   "-i", os.path.join(tmp, "%04d.jpg"), "-vf",
                   f"scale=270:-2,tile={cols}x{rows}:padding=6:margin=6:color=white",
                   "-frames:v", "1", "-q:v", "3", dest], check=False)
    return "contact-sheet.jpg" if res.returncode == 0 and os.path.exists(dest) else None


def audio_profile(path, duration):
    res = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af",
               "silencedetect=noise=-35dB:d=0.4,volumedetect", "-f", "null", "-"], check=False)
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", res.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", res.stderr)]
    if len(ends) < len(starts):
        ends.append(duration)
    silent = sum(max(0.0, e - s) for s, e in zip(starts, ends))
    mean = re.search(r"mean_volume: (-?[0-9.]+) dB", res.stderr)
    first_sound = 0.0
    if starts and starts[0] < 0.05 and ends:
        first_sound = ends[0]
    return {
        "silent_share": round(silent / duration, 2) if duration else None,
        "mean_volume_db": float(mean.group(1)) if mean else None,
        "first_sound_at_s": round(first_sound, 2),
        "silences": [{"start": round(s, 2), "end": round(e, 2)} for s, e in zip(starts, ends)],
        "note": "Audio is measured, not identified: this can't tell speech from music. "
                "Use the transcript (speech) and the frames/caption (named sound) for that.",
    }


def parse_subs(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    segs = []
    pat = re.compile(r"(\d+:)?(\d\d):(\d\d)[.,](\d{3})\s*-->\s*(\d+:)?(\d\d):(\d\d)[.,](\d{3})"
                     r"[^\n]*\n(.*?)(?:\n\n|\Z)", re.S)

    def secs(h, m, s, ms):
        return int((h or "0:")[:-1]) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    for m in pat.finditer(text):
        line = re.sub(r"<[^>]+>", "", m.group(9)).strip().replace("\n", " ")
        if line and (not segs or segs[-1]["text"] != line):
            segs.append({"start": round(secs(*m.group(1, 2, 3, 4)), 2),
                         "end": round(secs(*m.group(5, 6, 7, 8)), 2), "text": line})
    return segs


def transcribe(path, has_audio, workdir):
    if not has_audio:
        return {"source": None, "segments": [], "note": "No audio track."}
    base = os.path.splitext(path)[0]
    for ext in (".vtt", ".srt", ".en.vtt", ".en.srt"):
        if os.path.exists(base + ext):
            return {"source": f"subtitle file ({os.path.basename(base + ext)})",
                    "segments": parse_subs(base + ext)}
    for f in os.listdir(os.path.dirname(path) or "."):
        # same name plus a language tag only (reel.en.vtt), never reel2.vtt for reel.mp4
        if f.startswith(os.path.basename(base) + ".") and f.endswith((".vtt", ".srt")):
            p = os.path.join(os.path.dirname(path) or ".", f)
            return {"source": f"subtitle file ({f})", "segments": parse_subs(p)}

    wav = os.path.join(workdir, "audio16k.wav")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", path, "-vn", "-ac", "1",
         "-ar", "16000", wav], check=False)
    if not os.path.exists(wav):
        return {"source": None, "segments": [], "note": "Could not extract audio."}

    try:
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel(os.environ.get("WHISPER_MODEL", "base"), compute_type="int8")
        segments, info = model.transcribe(wav, vad_filter=True, word_timestamps=True)
        segs, words = [], []
        for s in segments:
            segs.append({"start": round(s.start, 2), "end": round(s.end, 2),
                         "text": s.text.strip()})
            words += [{"start": round(w.start, 2), "end": round(w.end, 2),
                       "w": w.word.strip()} for w in (s.words or [])]
        return {"source": "faster-whisper", "language": info.language, "segments": segs,
                "words": words}
    except ImportError:
        pass
    except Exception as e:  # model download blocked, etc. Try the next engine.
        print(f"video-eyes: faster-whisper failed ({e}); trying other engines.", file=sys.stderr)

    if shutil.which("whisper"):
        res = run(["whisper", wav, "--model", os.environ.get("WHISPER_MODEL", "base"),
                   "--output_format", "srt", "--output_dir", workdir], check=False)
        srt = os.path.join(workdir, "audio16k.srt")
        if res.returncode == 0 and os.path.exists(srt):
            return {"source": "whisper CLI", "segments": parse_subs(srt)}

    model_path = os.environ.get("WHISPER_CPP_MODEL")
    if shutil.which("whisper-cli") and model_path and os.path.exists(model_path):
        prefix = os.path.join(workdir, "wcpp")
        res = run(["whisper-cli", "-m", model_path, "-f", wav, "-osrt", "-of", prefix],
                  check=False)
        if res.returncode == 0 and os.path.exists(prefix + ".srt"):
            return {"source": "whisper.cpp", "segments": parse_subs(prefix + ".srt")}

    return {"source": None, "segments": [],
            "note": "No transcription engine found. Options: pip install faster-whisper; "
                    "or paste the platform's own captions/transcript; or work from the "
                    "frames (on-screen text often carries the script)."}


def ocr_hint(out_dir, frames):
    if shutil.which("tesseract") is None:
        return False
    for f in frames:
        res = run(["tesseract", os.path.join(out_dir, f["file"]), "-", "--psm", "11"],
                  check=False)
        words = " ".join(res.stdout.split())
        if len(re.sub(r"[^A-Za-z0-9]", "", words)) >= 4:
            f["ocr_hint"] = words[:240]
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="video file path, or a URL (needs yt-dlp)")
    ap.add_argument("--out", default=None, help="output folder (default: <video>-eyes/)")
    ap.add_argument("--scene", type=float, default=0.30,
                    help="cut sensitivity 0-1; lower finds more cuts (default 0.30)")
    ap.add_argument("--no-transcript", action="store_true")
    ap.add_argument("--no-ocr", action="store_true")
    args = ap.parse_args()

    need("ffmpeg")
    need("ffprobe")
    work = tempfile.mkdtemp(prefix="video-eyes-")
    src = args.source
    if re.match(r"https?://", src):
        src = fetch_url(src, work)
    elif not os.path.isfile(src):
        sys.exit(f"video-eyes: file not found: {src}")

    out = args.out or (os.path.splitext(os.path.abspath(args.source))[0] + "-eyes"
                       if not re.match(r"https?://", args.source) else "video-eyes-out")
    os.makedirs(out, exist_ok=True)

    meta = probe(src)
    dur = meta["duration_s"]
    cuts = detect_cuts(src, args.scene)
    shots = build_shots(cuts, dur)
    frames = extract_frames(src, sample_times(shots), os.path.join(out, "frames"))
    sheet = contact_sheet(frames, out)
    audio = audio_profile(src, dur) if meta["has_audio"] else None
    transcript = ({"source": None, "segments": [], "note": "Skipped (--no-transcript)."}
                  if args.no_transcript else transcribe(src, meta["has_audio"], work))
    ocr = False if args.no_ocr else ocr_hint(out, frames)

    # Word timings (faster-whisper) attribute speech to shots precisely; subtitle segments
    # are coarser, so a line that spans a cut is attributed by its midpoint.
    units = transcript.get("words") or [
        {"start": g["start"], "end": g["end"], "w": g["text"]} for g in transcript["segments"]]

    def said_between(a, b):
        return " ".join(u["w"] for u in units if a <= (u["start"] + u["end"]) / 2 < b)

    for s in shots:
        s["frames"] = [f["file"] for f in frames if s["start"] <= f["t"] < s["end"]
                       or (s is shots[-1] and f["t"] >= s["start"])]
        s["said"] = said_between(s["start"], s["end"] + (0.01 if s is shots[-1] else 0))

    hook_cuts = [c for c in cuts if c <= HOOK_WINDOW]
    hook_words = said_between(0, HOOK_WINDOW)
    first_speech = transcript["segments"][0]["start"] if transcript["segments"] else None

    report = {
        "tool": "video-eyes",
        "source": os.path.basename(src),
        "video": meta,
        "pacing": {
            "shots": len(shots),
            "avg_shot_s": round(dur / len(shots), 2) if shots else None,
            "cuts_per_10s": round(len(cuts) / dur * 10, 1) if dur else None,
            "scene_threshold": args.scene,
        },
        "hook_window": {
            "seconds": HOOK_WINDOW,
            "cuts": len(hook_cuts),
            "first_speech_at_s": first_speech,
            "words_spoken": hook_words or None,
        },
        "shots": shots,
        "frames": frames,
        "contact_sheet": sheet,
        "contact_sheet_order": [f["file"] for f in frames] if sheet else [],
        "audio": audio,
        "transcript": transcript,
        "ocr": "tesseract hints added per frame (verify against the image)" if ocr else None,
        "limits": [
            "Cuts come from visual change; fast pans or flashes can add false cuts, and soft "
            "dissolves can hide real ones. Check the contact sheet.",
            "Frames are samples, not the whole video: motion, gestures and timing between "
            "frames are inferred, so say so when it matters.",
            "Nothing here identifies a song or sound. Read the audio label on screen or ask.",
        ],
    }
    with open(os.path.join(out, "timeline.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    shutil.rmtree(work, ignore_errors=True)

    print(f"video-eyes: {len(shots)} shots, {len(frames)} frames, "
          f"transcript: {transcript['source'] or 'none'} -> {os.path.join(out, 'timeline.json')}")


if __name__ == "__main__":
    main()
