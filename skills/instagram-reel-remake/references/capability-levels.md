# Capability Levels: getting the video in and watching it

The skill runs in very different agents: Claude Code and OpenClaw can run commands, claude.ai
runs code in a sandbox, and some chat agents can only read images. Same skill, three levels.
Detect the level, say which one you're at, and never claim to have seen more than that level
allows.

## How to detect the level

1. Can you run a shell command? Try `ffmpeg -version`.
   - Works: **level 3** (or level 2 if you're in a sandbox without access to the user's files;
     the difference only matters for where the file comes from).
   - Command runs but ffmpeg is missing: offer the install line below, or drop to level 1.
2. No code execution at all: **level 1**.

## Getting the file (all levels)

| Platform | Easiest way to get the video | Notes |
|---|---|---|
| Instagram | Share > Download on the reel | Only when the creator allows downloads; a watermark is added. Otherwise screen-record. |
| TikTok | Share > Save video, or the URL with `yt-dlp` | Saved videos carry a watermark; fine for analysis. |
| YouTube Shorts | The URL with `yt-dlp` | Usually works without login. |
| Any | Screen recording | Always works. Trim the start/end so the timings line up. |

Don't ask for Instagram cookies, passwords or a logged-in browser export to make `yt-dlp` work.
It's fragile (cookies expire), and it puts the user's account at risk for a convenience the
Share > Download button already gives them.

## Level 3: shell (Claude Code, OpenClaw, Codex, Hermes)

Requirements: Python 3.8+ and ffmpeg. Everything else is optional.

```bash
# install ffmpeg if missing
brew install ffmpeg            # macOS
sudo apt install ffmpeg        # Debian / Ubuntu

# run (from the skill folder, or pass the full path to the script)
python3 scripts/video-eyes.py ~/Downloads/reel.mp4 --out remake/
python3 scripts/video-eyes.py "https://www.tiktok.com/@user/video/123" --out remake/   # needs yt-dlp
```

Optional extras, picked up automatically:

| Extra | What it adds | Install |
|---|---|---|
| `faster-whisper` | Transcript with word timings, so speech maps to the exact shot | `pip install faster-whisper` (downloads a small model on first run; `WHISPER_MODEL=tiny` for speed) |
| `whisper` CLI or `whisper.cpp` | Same, different engines | See their docs; whisper.cpp needs `WHISPER_CPP_MODEL=/path/to/ggml-model.bin` |
| A `.vtt`/`.srt` next to the video | Uses the platform's own captions; no model needed | `yt-dlp --write-auto-subs` writes these for TikTok/YouTube |
| `tesseract` | An OCR hint per frame | `brew install tesseract`; the agent should still read the frames itself |
| `yt-dlp` | URL input | `pip install yt-dlp` or `brew install yt-dlp` |

Useful flags: `--scene 0.2` finds more cuts (soft transitions), `--scene 0.45` fewer (shaky
handheld footage); `--no-transcript` skips speech.

### Reading the output

`timeline.json` holds:

- `video`: duration, size, aspect (9:16 expected), fps.
- `pacing`: number of shots, average shot length, cuts per 10 seconds.
- `hook_window`: cuts and words in the first 3 seconds, when speech starts.
- `shots[]`: start/end, frames inside it, what was said during it.
- `frames[]`: time, file, why it was sampled (shot start, held shot, hook window), OCR hint.
- `audio`: silent stretches, loudness, when sound first starts. It measures audio; it can't
  name a song or tell speech from music.
- `transcript`: source engine, segments, word timings when available.
- `limits`: read these back to the user when they matter.

Then **look at the frames**. `contact-sheet.jpg` shows them all at once in the order of
`contact_sheet_order`; open individual hook-window frames to read small on-screen text. The JSON
gives timing; only the images show what's on screen.

## Level 2: sandbox (claude.ai)

The user uploads the video into the chat. In the code sandbox:

1. Check ffmpeg: `ffmpeg -version`. If it's missing, try installing it (`pip install
   imageio-ffmpeg` provides a binary; point the script at it by putting its folder on PATH).
2. Run `video-eyes.py` on the uploaded file with `--no-transcript` if a whisper model can't be
   downloaded in that sandbox.
3. No transcript? Ask the user to paste the reel's captions (Instagram shows auto-captions on
   most reels) or work from the on-screen text in the frames.

If uploads of video files aren't accepted in that client, drop to level 1.

## Level 1: eyes only (screenshots)

Ask for, in order of value:

1. The **first frame** (what shows before anyone taps).
2. A screenshot at **1 to 2 seconds** (the hook's on-screen text).
3. One screenshot **per new scene** (3 to 6 total).
4. The **last frame** (CTA or loop).
5. The **caption** (pasted) and, if spoken, what's said in the first sentence.
6. A screenshot of the **stats** and the **top comments**.

Build the beat sheet from these, and say plainly: "I'm working from 5 screenshots, so cut timing
and pacing are estimates." The remake can still be strong; the timing just comes from the
user's description instead of measured cuts.
