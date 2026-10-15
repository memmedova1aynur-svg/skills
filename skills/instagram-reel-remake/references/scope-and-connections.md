# Scope and Connections

## The job

Turn a proven short video into the user's own original version, end to end: get the file in,
watch it, explain why it worked, rebuild it beat-matched in their voice, check it's original,
publish it with confirmation, and read the results back. One skill, no other skills needed.

## Does

- Runs `scripts/video-eyes.py` (free: Python + ffmpeg, optional local whisper) to extract shots,
  frames, pacing, hook-window stats and a transcript.
- Reads frames directly (multimodal) for on-screen text, framing and visual hooks.
- Scores whether the source is an outlier and says no when it isn't.
- Writes the beat sheet, the remake script, 3 alternative hooks, the shot list, on-screen text,
  caption, cover brief, audio direction and edit plan (`writing-and-publishing.md`,
  `remake-recipes.md`).
- Enforces the originality gate.
- Publishes with WoopSocial after explicit confirmation (`woopsocial.md`): Instagram Reel,
  TikTok draft, YouTube Short.
- Reads post metrics back from WoopSocial and keeps a one-line lesson log.
- Cuts the user's own clips together with ffmpeg when they hand them over and a shell is
  available.

## Doesn't

- Repost, re-upload or reuse any part of the source video, audio, voice or text.
- Download in bulk, scrape accounts, or use logged-in sessions or cookies.
- Use paid services, API keys or accounts to watch the video. (Publishing needs a WoopSocial
  connection; without one, the user gets the files and posts them by hand.)
- Identify songs, or extract a sound to reuse.
- Film the video, or generate footage.
- Promise views or virality. Invent metrics.

## Inputs it reads

- Brand or voice notes if the workspace has them (`brand-profile.md` or similar); otherwise the
  three quick questions in Step 0.
- The source video or screenshots, its visible stats, the creator's follower count, the top
  comments.
- The user's remake log, if one exists, to reuse lessons.

## Outputs it writes

- `remake/timeline.json`, `remake/frames/`, `remake/contact-sheet.jpg` (from video-eyes).
- The remake pack: beat sheet, script, hooks, shot list, on-screen text, caption, cover brief,
  edit plan, publish block.
- After publishing: one line per remake in `remake-log.md` (date, source, outlier score, mode,
  metrics with `collectedAt`, lesson).

## Publishing

With WoopSocial, as described in `woopsocial.md` (bundled in this folder): health check,
upload media, validate, explicit confirmation, create the post, then read metrics with
`social_account_posts_list`. Metrics WoopSocial doesn't return (watch time, retention, follower
growth) come from the platform's own insights.
