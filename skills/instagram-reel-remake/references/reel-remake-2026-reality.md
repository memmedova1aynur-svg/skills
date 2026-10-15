# Reel Remakes: the 2026 reality (verify-quarterly)

What changed, what's allowed, and what breaks. Re-check every quarter; platforms move fast.

## Instagram's originality rule (announced April 30, 2026)

- Instagram extended its Reels originality policy to photos and carousels. **Original** means
  wholly created or **materially altered** by the poster. Commentary, voiceover or real editing
  on a third-party clip can qualify; **cropping, resizing, adding a watermark or a credit tag
  does not.**
- When Instagram finds **two or more identical pieces of content, it recommends only the
  original.** Reposts can still reach the poster's followers but stop being pushed to
  non-followers, and may carry attribution labels.
- Some marketing blogs claim a hard threshold (for example "10+ reposts in 30 days removes you
  from recommendations"). That number was **not** in Instagram's announcement or major tech
  coverage at the time of writing; treat it as unconfirmed.

What this means for remakes: a remake that passes the originality gate (new footage, new words,
the user's substance, shared structure only) is original content. A re-upload with credit is
not, and it gives the reach to the original creator.

Sources: PetaPixel (2026-04-30), TechCrunch coverage of the update, Planoly's summary.

## Copyright and terms

- Reposting someone else's reel without permission is the creator's copyright, credit or not.
- Formats, structures and hook patterns ("3 signs your…", POV, before/after) are not owned by
  anyone; specific footage, recordings and text are.
- Bulk automated downloading conflicts with Instagram's terms. This skill works one reel at a
  time from a file the user saved with the app's own download button or a screen recording.
- This is general information, not legal advice. For paid campaigns or anything contested,
  check with someone qualified.

## Getting the video (what actually works)

- **Instagram:** Share > Download saves public reels when the creator hasn't turned downloads
  off (with a watermark). `yt-dlp` and similar tools usually need a logged-in session for
  Instagram, even for public reels, and sessions expire; this skill doesn't use that path.
- **TikTok and YouTube:** `yt-dlp` generally works without a login, and can save the platform's
  auto-captions as a subtitle file, which `video-eyes.py` uses before running whisper.
- **Screen recording** works everywhere and is the reliable fallback.

## What agents can actually do

- An agent **cannot watch a video from a link**. It sees frames and text it's given. That's why
  this skill extracts frames and a transcript first.
- **Shell agents** (Claude Code, OpenClaw, Codex, Hermes) can run ffmpeg and a local whisper
  model: free, private, no keys.
- **Sandboxed agents** (claude.ai) can run code on uploaded files; network access for model
  downloads varies by settings, so transcription may need the reel's own captions instead.
- **Chat-only agents** work from screenshots.

## Publishing realities

- **TikTok:** trending sounds can't be attached through the API. Upload as a draft
  (`MEDIA_UPLOAD`) and add the sound in the app before posting.
- **Instagram:** Reels publish with caption and cover through WoopSocial; the
  trending audio library, Share-to-Feed tweaks and tagging stay in the app.
- **AI disclosure:** if the remake uses AI-generated footage or voice, disclose it. On TikTok
  WoopSocial applies the AI label automatically; elsewhere, label it in-app.

## What the platforms reward in 2026 (verify-quarterly)

- Watch time and completion, then shares and saves, matter more than likes for recommendations
  on both Instagram and TikTok.
- Originality is now an explicit ranking factor on Instagram (above).
- Search keywords in the caption and on-screen text help discovery (caption rules: `writing-and-publishing.md`).
