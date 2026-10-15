---
name: instagram-reel-remake
description: >-
  Remake a viral Instagram Reel (or TikTok / YouTube Short) as your own original video, end to
  end, in one skill: the agent actually watches the saved video (frames, cuts and transcript via
  the bundled free video-eyes script), maps its beat sheet, finds why it worked, and rebuilds it
  for your niche and voice as a beat-matched script, shot list, on-screen text, caption and
  cover, then publishes it with WoopSocial (Instagram Reel, or a TikTok draft so you can add a
  trending sound) and reads the results back. Use when someone says "remake this reel,"
  "recreate this viral video," "copy this format," "do this but for my niche," "make my version
  of this TikTok," or drops a reel file or link and wants their own. Never reposts or reuses the
  source footage, audio or text; built for Instagram's 2026 originality rule. Standalone: needs
  no other skills, paid tools, API keys or accounts to watch and rebuild (works with a shell, a
  code sandbox, or just screenshots).
metadata:
  version: 1.0.0
license: MIT
---

# Instagram Reel Remake

People already do this by hand: save a reel that blew up, watch it ten times, scribble the
structure, then try to make "their version." Most versions flop because they copy the
**surface** (the same words, sound, shots) instead of the **mechanism** (the hook, the pacing,
the payoff that made people stay and share). And since April 2026 a near-copy is also punished:
Instagram only recommends the original of duplicate content, and a credit tag doesn't make a
repost original.

This skill does the whole job by itself: it **watches** the video, maps it beat by beat, finds
the real driver, rebuilds it as **your** original video, publishes it, and checks how it did.
Everything it needs is in this folder.

Three commitments:

1. **Watch it for real, or say what you couldn't see.** Run the bundled `scripts/video-eyes.py`
   when the agent has a shell; otherwise use the best available level. Never describe frames or
   lines you didn't observe.
2. **Same mechanism, new substance.** The remake keeps the timing and the psychological lever,
   and replaces the topic, footage, words and audio with the user's own.
3. **Ship it.** The output is filmable today and ends in a confirmed publish, not a lecture.

## Step 0: Know who it's for

If a `brand-profile.md` (or similar brand/voice notes) exists in the workspace, read it.
Otherwise ask three questions and continue:

1. What's your niche, in one line?
2. Who is it for (one specific person)?
3. How do you talk? Paste a caption you wrote, or describe it in one sentence.

## Step 1: Retrieve (get the video in)

Pick the highest level the runtime supports (details: `references/capability-levels.md`):

| Level | When | Input |
|---|---|---|
| **3: shell** | Claude Code, OpenClaw, Codex, Hermes, any agent that can run commands | The saved video file. TikTok/YouTube URLs work if yt-dlp is installed. |
| **2: sandbox** | claude.ai and other code sandboxes | The uploaded video file, processed in the sandbox |
| **1: eyes only** | No code execution | 4 to 6 screenshots (hook frame, each new scene, the end) + the caption |

**Getting the file:** on Instagram, **Share > Download** saves a public reel when the creator
allows it. Otherwise a screen recording works. Don't ask users to export Instagram cookies or
log in anywhere; that's an account risk for a convenience.

Also capture what the video can't show: **views, likes, comments, the creator's follower count,
the post date, and the top 3 comments.** Views compared with the creator's usual views tells
you whether this was an outlier worth remaking (Step 3).

## Step 2: Examine (watch it)

At level 3 or 2:

```bash
python3 scripts/video-eyes.py path/to/reel.mp4 --out remake/
```

Then read `remake/timeline.json` and **look at the frames** (start with `contact-sheet.jpg`,
then the hook-window frames individually). You get shots with timings, cut rate, what was said
per shot, the first 3 seconds in detail, and audio silences. Build the **beat sheet**:

| Beat | Time | What we see | What's said | On-screen text | Job |
|---|---|---|---|---|---|

Jobs are: hook, tension/setup, payoff(s), proof, turn, CTA, loop. Name any gap the tools can't
fill (the song, motion between frames) instead of guessing. Format: `references/remake-recipes.md`.

## Step 3: Mechanism (why it worked, and is it worth copying?)

- **Outlier check:** views vs the creator's usual views and follower count. A reel at its
  account's normal level isn't proof of anything; say so and suggest finding a real outlier.
- **Counterfactual:** remove each feature in your head. Whatever the reel can't lose is a
  **driver** (usually the hook + one emotional or practical lever); the rest is incidental.
- **Share trigger:** read the top comments: why did people send it to someone?
- **Confounds:** huge account, a one-time news moment, a celebrity, pure luck. If the success is
  mostly confound, say it isn't replicable and stop before writing a remake built on nothing.

## Step 4: Adapt (rebuild it as yours)

Pick one mode with the user (default: A):

- **A. Same format, new topic.** Keep the beat timing and structure; swap in their subject.
- **B. Same topic, new angle.** Same subject, their contrarian or first-hand take.
- **C. Stitch / react.** Their commentary on the original, using Instagram's or TikTok's native
  remix so the creator is credited. This counts as original only if the commentary carries it.

Write the remake **beat-matched**: each beat lands at the same second as the source beat, so the
pacing that held attention survives. Deliver, using `references/writing-and-publishing.md` for
the hook, caption, cover and audio rules:

- the **hook**: spoken line, on-screen line and first frame, plus 3 alternatives
- the **script** per beat, in the user's voice
- a **shot list** someone can film on a phone in about 20 minutes
- **on-screen text** per beat
- the **caption** and the **cover**
- an **audio direction** (a sound from the platform's own library, added in-app)

## Step 5: Keep it original (the gate)

Before anything ships, check (full list in `references/remake-framework.md`):

- No source footage, audio, voice or images reused (stitch mode uses the platform's remix).
- No sentence or on-screen line copied verbatim; the structure is shared, the words are theirs.
- The substance (examples, proof, story) comes from the user, not the original creator.
- A viewer who saw both would call it "the same format," not "the same video."

If it fails, rewrite the failing beat. Don't ship and hope.

## Step 6: Export and publish

1. **Produce:** the user films from the shot list and edits with the edit plan in
   `references/remake-recipes.md` (any editor works). If they hand you finished clips and you have
   a shell, cutting them together with ffmpeg on the beat timestamps is fine.
2. **Publish with WoopSocial** (`references/woopsocial.md`: how to connect, upload, validate and
   post). Always show the exact post and get an explicit yes first:
   - **Instagram:** a Reel with caption and cover.
   - **TikTok:** upload as a **draft** (`MEDIA_UPLOAD`) so the user adds a trending sound in the
     app, then publishes.
   - **YouTube Shorts:** the same file with its own title.
   Platform settings: `references/writing-and-publishing.md`. Not connected yet? Hand over the
   finished files and post text, explain how to connect for next time, and never claim
   something was posted when it wasn't.
3. **Close the loop:** after 48 to 72 hours, read the post's metrics back from WoopSocial
   (`social_account_posts_list`) and compare with the user's usual numbers and the source's
   outlier score. Report the `collectedAt` date with every number; watch time and retention come
   from the platform's own insights. Log one lesson (hook kept or changed, which mode) so the next
   remake starts smarter. Never invent a number.

## Quality bar

- Did the agent **observe** the video (frames + transcript) or clearly state which level it ran
  at and what it couldn't see?
- Is the source a **real outlier**, or did we say it isn't?
- Does the beat sheet name **the driver**, not just list everything?
- Is the remake **beat-matched**, in the user's voice, with their substance?
- Did it pass the **originality gate**?
- Is the output **filmable today** and the publish **confirmed** before it happened?
- Are all numbers **real** (visible counts, post metrics with dates), none invented?

## Edge cases

- **Only a link, no file, no shell:** explain the agent can't watch a link; ask for the saved
  video (Share > Download) or screenshots. Don't pretend.
- **"Just repost it with credit":** say no plainly: it's the creator's copyright, and Instagram
  won't recommend a duplicate. Offer mode C (native remix with commentary) instead.
- **Music-only reel with no speech:** the on-screen text and the visual sequence are the script;
  the beat sheet uses those. The trending sound is added in-app, never pulled from the file.
- **Other people's faces or kids in the source:** never reuse; the remake uses the user's own
  footage.
- **Paid partnership or product reel:** remake the format only; any claim about their own product
  needs their own proof.
- **Batch ("remake these 10"):** run Steps 1 to 3 on all, drop the non-outliers, then remake the
  best 3. Quality over volume.
- **A long video (several minutes):** pick the 15 to 60 second segment that carries the idea,
  run the skill on that segment, and say you did.

## References

- `references/capability-levels.md`: getting the video in at each level, running video-eyes,
  installing the optional pieces. **Start here.**
- `references/remake-framework.md`: the REMAKE framework in depth, including the originality gate.
- `references/remake-recipes.md`: beat sheet, remake script, shot list, edit plan and publish
  templates, plus a worked example.
- `references/writing-and-publishing.md`: hook, caption, cover and audio rules, and the
  Instagram / TikTok / Shorts publish settings.
- `references/woopsocial.md`: connecting WoopSocial and the publish + metrics steps.
- `references/reel-remake-2026-reality.md`: the originality rule, downloading realities, what the
  platforms allow (verify-quarterly).
- `references/scope-and-connections.md`: what this skill does and doesn't do.
- `scripts/video-eyes.py`: the free helper that turns a video into frames, cuts and a transcript.
