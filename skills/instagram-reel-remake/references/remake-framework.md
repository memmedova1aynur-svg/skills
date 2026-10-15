# The REMAKE Framework

Six steps, in order. Skipping one is how remakes become either flops (skipped M) or copies
(skipped K).

| | Step | Question it answers | Output |
|---|---|---|---|
| **R** | Retrieve | What exactly are we looking at? | The video at the highest capability level + its stats and top comments |
| **E** | Examine | What happens, second by second? | Beat sheet |
| **M** | Mechanism | Why did it work, and will it work for us? | Outlier score, 1 to 2 drivers, share trigger, go/no-go |
| **A** | Adapt | What's our version? | Beat-matched script, shot list, on-screen text, caption, cover, audio direction |
| **K** | Keep original | Is it ours? | Passed originality gate |
| **E** | Export | How does it get out and what did it teach us? | Confirmed publish, metrics read-back, a logged lesson |

## R: Retrieve

Minimum viable input: the video (or screenshots) plus **views and follower count**. Without the
numbers, you can't tell an outlier from an average post, and you'll remake noise.

**Outlier score** = views / follower count, compared with the creator's other recent reels.
Rules of thumb (verify per niche): a reel at roughly 1x the creator's usual views is just a post;
3x or more is worth studying; 10x or more is a real outlier. A small account with a big hit is
more useful to copy than a big account's routine post: its success came from the content, not
the audience.

## E: Examine

Build the beat sheet from `timeline.json` + frames. Label each beat with its **job**:

- **Hook** (0 to 3s): the first frame, the first words and the on-screen line. Note what
  creates the open loop: a question, a claim, a conflict, a visual surprise.
- **Setup / tension**: why should I care, what's at stake.
- **Payoff(s)**: the value, reveal or punchline. Many reels pay off in small steps to hold
  attention.
- **Proof**: a result, a screen, a before/after, a credible face.
- **Turn**: the twist that makes it shareable.
- **CTA**: what it asks (often nothing, or "follow for part 2").
- **Loop**: does the ending flow back into the start (rewatches)?

Measure what the tools give you: cuts per 10 seconds, when speech starts, how many cuts land in
the hook window. A 2026 reel that opens on a talking head with no on-screen text and no cut for
4 seconds is rare among outliers; note it when you see it, because it means something else is
carrying the hook.

## M: Mechanism

Use the counterfactual test: for each feature (sound, topic, face, edit style, the hook line,
the text overlay), ask "if this were gone, would it still have popped?" What it can't lose is a
driver. Usually it's the hook plus one lever:

- **Practical value**: saves ("I need this later").
- **Identity**: shares ("this is so me / so you").
- **High-arousal emotion**: awe, anger, humor.
- **Social currency**: knowing it makes you look smart.
- **Story with a turn**: people stay to see how it ends.

**Go/no-go:** if the outlier score is low, or the success is mostly a confound (huge account,
news moment, celebrity, luck), stop and say so. A remake built on a non-mechanism wastes a
filming session.

## A: Adapt

**Beat-matching:** keep each beat at the same timestamp (within about half a second) as the
source. Pacing is part of the mechanism; a remake that takes 6 seconds to land a hook the source
landed in 2 has removed the thing that worked.

**Choose the mode:**

| Mode | Use when | Watch out for |
|---|---|---|
| A. Same format, new topic | The structure is the driver (list, reveal, POV, before/after) | The topic must matter as much to your audience as the original's did to theirs |
| B. Same topic, new angle | The topic is the driver and you have a real take | Must be a real position or experience, not a reworded copy |
| C. Stitch / react | The original is so known that reacting is the content | Must carry real commentary; native remix only, never re-upload |

**Write in the user's voice** (their brand notes, or the Step 0 answers). Their examples, their numbers,
their story. If they have none for this topic, mode A on a topic where they do is better than a
hollow remake.

## K: Keep original (the gate)

Pass every line before publishing:

1. **Footage:** none of the source video, images or faces appear (except through the platform's
   native remix in mode C).
2. **Audio:** the source's voice and original audio are not reused. A trending library sound
   is added in-app by the user, not extracted from the file.
3. **Words:** no sentence or on-screen line is copied verbatim. Shared structure ("3 signs
   your…") is fine; shared sentences are not.
4. **Substance:** the examples, proof and story are the user's own.
5. **Viewer test:** someone who saw both would say "same format," never "same video."
6. **Claims:** any result, number or promise in the remake is true for this user.

Fail any line: rewrite that beat. This gate is also what keeps the remake eligible for
recommendations under Instagram's 2026 originality rule.

## E: Export

Produce (film and edit), then publish with WoopSocial (`woopsocial.md`) after explicit
confirmation. TikTok goes as a draft (`MEDIA_UPLOAD`) so the trending sound is added in-app.

After 48 to 72 hours, read the metrics back and write one line to the user's remake log:

```
2026-10-20 | source: @creator reel (12x outlier) | mode A | hook kept | 3.1k views at 48h (collectedAt 2026-10-22) vs usual 900 | lesson: list format works, my face in frame 1 beat text-only
```

Over a few weeks the log shows which formats and modes work for this account. That log is
worth more than any single remake.
