---
name: occasion-posts
description: >-
  Use to make a post or carousel for a specific day: a national holiday, a remembrance day, a
  religious holiday, an awareness day or a niche day (Novruz, Yeni il, 20 Yanvar, 1 iyun, 2
  aprel autism day, Bilik günü, coffee day...). Run when the user says "post for Novruz,"
  "what's coming up," "holiday post," "awareness day carousel," "təbrik postu," "anma postu,"
  "bayram karuseli," or needs the right image for a day. Ships a calendar (Azerbaijan, child
  development and health, international, niche days) with tone, palette, motifs, angles, what
  to avoid and AI image prompts per day; a script that lists upcoming days and scaffolds a
  ready spec; and tone rules the renderer enforces (no sales, jokes or confetti on remembrance
  days). Uses the MARK framework. Whether to post at all is seasonal-and-moment-marketing;
  rendering is carousel-builder; copy is carousel-writer; image generation routes through
  image-prompt. Never invents a movable date or a historical fact.
metadata:
  version: 1.0.0
license: MIT
---

# Occasion Posts

A day-specific post is judged in one glance: does this brand understand what today is? The
wrong symbol, a confetti graphic on a day of mourning or a stock "Nowruz" table from another
country tells the audience the post was made by someone who doesn't. This skill makes the
right call for the day, then renders it.

Three principles:

1. **Tone before design.** Every day has a tone: celebration, awareness, religious or
   remembrance. Tone decides palette, motifs, slide types and the ask. The renderer enforces it.
2. **The right image, from the most honest source.** The user's own photo first; then an AI
   image generated from a culturally checked prompt; then the built-in motif library, which is
   always correct and always on hand.
3. **Never invent a date or a fact.** Movable days (Novruz and the çərşənbələr, Ramazan and
   Qurban bayramı) are announced each year. Historical numbers come from an official source or
   stay out.

## Step 0 — Read the foundation

Load the brand kit and the voice. Check whether the brand has standing to speak on the day:
`seasonal-and-moment-marketing` owns the "should we post at all" gate. A dental clinic posting
about autism day needs a real angle, or silence.

## Step 1 — M: Match the day

```bash
node scripts/upcoming.cjs --days 45 --niche child-development,speech
node scripts/upcoming.cjs --show autizm-gunu
```

The list shows each day's tone, the prepare-by date, motifs and notes (clashes such as 27
September being both Anım günü and World Tourism Day). Movable days print **VERIFY** with the
rule; look up the official date for the year before you schedule anything.

## Step 2 — A: Assign the tone

| tone | days | allowed | not allowed |
|---|---|---|---|
| celebration | Novruz, Yeni il, 1 iyun, national days | full palette, confetti, offers if the brand sells | offers that replace the greeting |
| awareness | 2 aprel, 21 mart, mental health day | education, myth/fact, resources | jokes about the condition, cure claims |
| religious | Ramazan, Qurban | calm greeting, family, sharing | memes, sales-first posts, decorative use of sacred symbols |
| remembrance | 20 Yanvar, 26 Fevral, 31 Mart, 27 Sentyabr | dark sober palette, carnation, candle, flag; a line of remembrance | sales, jokes, confetti, bright colour, "save this", realistic AI images of the tragedy |

Set `"tone"` in the spec. For remembrance the renderer swaps in a fixed dark palette and the
QA fails on posters, memes, quizzes, stats, confetti and save/follow/link asks. On a
remembrance day also pause the scheduled promotional posts (`scheduling-and-queue`).

## Step 3 — R: Render the visual

Pick the image source in this order:

1. **The user's photo** (the team, the classroom, the café's real xonça). Most authentic.
   Use `"image"` on the cover or greeting. Children's faces only with parental consent.
2. **AI image.** Use the day's `ai_prompt` from the calendar as the base, refine it with
   `image-prompt`, generate with whatever image tool is connected (an MCP image tool or one of
   the image-tool skills), save the file, reference it as `"image"`. Check the result against
   the day's `avoid` list before using it. Disclose AI imagery where the platform requires it.
3. **Motif library** (in `carousel-builder`): `"motif": "semeni"` and friends. Free, offline,
   culturally checked, recolour-free. The default for remembrance days.

Scaffold the spec, then write the real copy into it:

```bash
node scripts/upcoming.cjs --spec novruz --format post --brand brands/client.json
node scripts/upcoming.cjs --spec autizm-gunu --format carousel --brand brands/client.json
```

The scaffold carries the tone, the day's palette, the motif and an `_occasion` block (angles,
avoid list, AI prompt, verify flag). Replace every capitalised placeholder, then render with
`carousel-builder`. A greeting post is one `greeting` slide; a carousel follows
`carousel-writer`'s structure with the day as the hook.

## Step 4 — K: Keep it right

Before handing over:
- QA exit code 0 from `carousel-builder` (tone rules included).
- The date is checked for movable days; facts and numbers have an official source.
- The `avoid` list for the day is clear (no puzzle piece on autism day, no haft-sin on Novruz,
  no logo on the flag, no stock image passed off as the client's).
- The caption matches the tone (`caption-writer`): no hashtags stuffing on remembrance days.
- Nothing is scheduled without the user's explicit confirmation.

## Quality bar — self-check

- Did the brand have a real reason to post today? If not, did you say so?
- Is the tone right, and did the renderer's tone QA pass?
- Is the image the most honest available, and culturally correct for Azerbaijan?
- Are movable dates verified and facts sourced?
- Remembrance: dark palette, no ask, no promotion, scheduled promos paused?

## Edge cases & pushback

- **"Add a discount to the 20 Yanvar post"** → refuse the discount; offer a quiet
  remembrance post and moving the promotion to another day.
- **Two days collide** (21 March: Novruz and Down Syndrome Day) → two separate posts, never
  one merged graphic.
- **No date for Ramazan bayramı yet** → plan with "date TBC", schedule only after the
  official announcement.
- **AI image shows the wrong culture** (haft-sin, Western Easter eggs) → regenerate with the
  prompt's negatives, or use the motif library. Do not ship "close enough".
- **Client wants the puzzle piece for autism day** → explain the community objection briefly,
  offer the infinity symbol; the client decides, and you note the risk.

## Related skills

- `seasonal-and-moment-marketing` — which days are worth it, planned a year ahead.
- `carousel-builder` — renders the post, enforces tone, holds the motif library.
- `carousel-writer`, `carousel-strategy`, `hook-writer` — copy and structure for carousels.
- `image-prompt` — refines the AI prompt for whichever image tool is connected.
- `caption-writer`, `scheduling-and-queue` — caption, then scheduling on confirmation.

## References

- `references/scope-and-connections.md` — what this skill does and hands off.
- `references/occasion-content-2026-reality.md` — cultural and sensitivity rules by day type.
- `references/the-mark-framework.md` — MARK in detail, the calendar fields, the scripts.
- `references/recipes-and-prompts.md` — post recipes per day type and the AI prompt rules.
