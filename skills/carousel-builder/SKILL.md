---
name: carousel-builder
description: >-
  Use to turn carousel copy into finished, upload-ready slide files in one command: 1080x1350
  PNGs, a PDF (LinkedIn document post), a contact sheet and a QA report, on-brand, with no
  design tool. Run when the user says "make the slides," "design this carousel," "render the
  carousel," "export the carousel," "carousel PNGs," "make it look professional," "build a
  carousel template," "brand kit for carousels," or has carousel copy and needs the files. Ships
  six themes (minimal, bold, editorial, tweet, data, steps), a per-client brand kit (colours,
  fonts, logo, handle), auto-fit text, and QA that blocks overflow, low contrast, missing glyphs
  (Azerbaijani, Turkish, Cyrillic), unsafe edges and unsourced stats. Uses the BUILD framework.
  Copy comes from carousel-writer; the reusable visual system across asset types is
  design-and-templates; Canva-first teams use canva; caption to caption-writer; scheduling to
  scheduling-and-queue. Renders locally with Playwright; never publishes.
metadata:
  version: 1.0.0
license: MIT
---

# Carousel Builder

`carousel-writer` decides what each slide says. This skill turns that into **files you can
upload**: a set of 1080x1350 PNGs, a PDF and a contact sheet, rendered from HTML templates
with Playwright and checked before anyone sees them.

The bar is "looks like a designer made it" with **zero design work per post**. That comes from
three things, not from talent:

1. **A brand kit, set once.** Colours, fonts, logo and handle live in one JSON file per client.
   Every carousel reads it, so the hundredth post still looks like the first.
2. **A small set of strong themes.** Six layouts that already have hierarchy, spacing and
   rhythm solved. Pick one per series and keep it; consistency is what reads as professional.
3. **A QA gate.** Text that overflows, a font missing the letter `ə`, grey-on-grey contrast or a
   stat with no source is caught by the build, not by a follower.

## Step 0 — Read the foundation

Load `brand-profile` output and the voice if they exist. If the user has carousel copy, use it.
If they have only an idea, write the copy first with `carousel-writer` (cover via
`hook-writer`), then come back here. Do not design around missing copy.

## Step 1 — B: Brand kit (once per client)

Look for an existing kit (`brands/<client>.json`). If there is none, create it from the
template in `assets/examples/brand-kit.example.json`: name, handle, language, five colours,
two fonts, optional logo. Ask only for what you cannot infer; default the rest. The field
reference and font advice are in `references/the-build-framework.md`.

To scaffold a fresh working folder: `node scripts/build-carousel.cjs --init <dir>`.

**Language matters.** Set `"language"` (`az`, `en`, `ru`, `tr`). It sets the swipe and save
labels and makes uppercase correct (`i` → `İ` in Azerbaijani and Turkish). Pick fonts that cover
the alphabet; the QA fails the build when a glyph is missing.

## Step 2 — U: Use the copy, map it to slide types

Write `carousel.json`. Each slide is one of nine types:

| type | use it for | fields |
|---|---|---|
| `cover` | the hook | `title`, `kicker`?, `subtitle`?, `image`? (full-bleed photo) |
| `text` | one idea | `title`, `body`? |
| `list` | steps, items | `title`?, `items`, `numbered`? |
| `stat` | one number | `value`, `label`, `source`, `kicker`? |
| `quote` | a line worth sending | `quote`, `author`? |
| `compare` | before/after, myth/fact | `title`?, `left{label,items}`, `right{label,items}` |
| `image` | a photo or screenshot | `src`, `title`?, `caption`?, `alt`? |
| `recap` | the screenshot slide | `title`, `items`, `kicker`? |
| `cta` | the one ask | `title`, `body`?, `action`?, `icon`? (save, share, comment, follow, link) |
| `greeting` | occasion card, single post | `title`, `message`?, `motif`/`image`?, `kicker`?, `signature`? |
| `poster` | ad, announcement, event | `title`, `details`? (`{label,value}`), `badge`?, `action`?, `contact`?, `motif`/`image`? |
| `meme` | humour, familiar situation | `caption`, `image`/`motif`?, `bottom`?, `credit`? |
| `comic` | dialogue, mini story | `panels` (2-4 × `{text, image/motif}`), `title`? |
| `quiz` / `answer` | scenario test, choice | `question`, `options` (2-4); answer adds `correct` (A-D), `explanation` |
| `table` | cheat sheet, comparison grid | `rows`, `columns`?, `title`?, `note`? |
| `annotated` | worksheet or screenshot explained in place | `image`, `notes` (1-5 × `{x, y, text}`, % of the image) |

`**word**` highlights in the accent colour. `"accent": true` flips any slide to the accent
background for a mid-carousel beat.

Stories: `--size story` (1080x1920) keeps text out of Instagram's top bar and reply bar and
fails QA on anything placed there. A `text` slide with `"reserve": "poll"` (or `question`,
`link`) leaves an empty band for a real sticker added by hand in the app; never draw a sticker.
`--jpeg` writes JPEG files, the only image format Instagram's publishing API accepts.

Spec-level switches: `"format": "post"` for a single-image post (no counter, swipe or
carousel checks); `"tone"` (`celebration`, `awareness`, `religious`, `remembrance`) where
remembrance swaps in a sober dark palette and the QA blocks posters, memes, quizzes, stats,
confetti and save/follow/link asks; `"palette"` to override brand colours for one post;
`"ornament": "<motif>"` to scatter a motif faintly. `"motif"` places an illustration from the
built-in library (`assets/motifs/`: səməni, tonqal, şam, qərənfil, şarlar, yolka, qar,
sonsuzluq, ürək, kitab, ulduz, bayraq, nar, şəkərbura, lalə, kublar, günəş, konfetti, hilal).
Which type and format a topic needs is decided first in `carousel-strategy`; day-specific
posts come from `occasion-posts`.

The finishing that makes it read as designed is built in, not per-post work: an author badge
and page counter on every slide, a line that runs continuously across slide edges (the
carousel swipes as one piece), faint oversized slide numbers, paper grain, card shadows, a
swipe button, crisp SVG icons, and a profile card on the CTA. Themes tune or switch these off. Full spec and recipes: `references/themes-and-recipes.md`.

## Step 3 — I: Identify the theme

`node scripts/build-carousel.cjs carousel.json --theme all` renders the same copy in all six
themes and writes `themes.png` for a side-by-side pick. Match theme to content, not taste:

- **minimal**: experts, services, premium. The safe default.
- **bold**: hot takes, myth-busting, lists that should shout.
- **editorial**: essays, stories, opinion.
- **tweet**: founders and personal brands; reads as a native text post.
- **data**: stats, research, results.
- **steps**: how-tos and processes (auto-numbers the points).

Then fix the theme in the spec and keep it for the series.

## Step 4 — L: Launch the build

```bash
node scripts/build-carousel.cjs carousel.json            # theme and size from the spec
node scripts/build-carousel.cjs carousel.json --theme bold --size square --out out/
```

Output: `slide-01.png` … , `carousel.pdf`, `contact-sheet.png`, `qa.json`, and `carousel.html`
(the fitted source, for hand tweaks). Needs Node 18+ and Playwright with Chromium. Fonts come
from Google Fonts; offline or for licensed brand fonts, add files under `fonts.files`.

## Step 5 — D: Debug with QA, then hand off

Exit code 0 means shippable; 1 means errors. **Never hand over a build with errors.** Fix the
copy, not the template: errors almost always mean too many words. Look at `contact-sheet.png`
yourself before showing the user; QA catches mechanics, not taste. What each check means and
how to fix it: `references/the-build-framework.md`.

Then hand off:
- Caption → `caption-writer` (alt text for the cover goes with it).
- Schedule → `scheduling-and-queue`. Nothing is scheduled or published without the user's
  explicit confirmation.
- LinkedIn → upload `carousel.pdf` as a document post (copy via `linkedin-post-writer`).

## Quality bar — self-check

- Brand kit used, not ad-hoc colours; one theme for the whole series?
- QA exit code 0; every warning either fixed or consciously accepted and told to the user?
- Cover readable on the contact sheet at thumbnail size?
- Every `stat` slide has a real, checkable source? No invented numbers.
- Recap slide stands alone as a screenshot? One CTA, one ask?
- You looked at the contact sheet before handing it over?

## Edge cases & pushback

- **"Make the text smaller so it fits"** → the build already shrinks to fit. When it warns, the
  answer is fewer words or a split slide, not 20px type.
- **Brand font lacks a letter** (`ə`, `ğ`, `ı`) → keep the brand font for headings only if it
  passes; otherwise pair a covering font. Never ship a fallback glyph.
- **No Node or Playwright** → install them (`npm i -g playwright && npx playwright install
  chromium`), or fall back to `canva` / `design-and-templates` with the same brand kit values.
- **AI-generated photos on `image` slides** → disclose per platform rules; generation lives in
  `image-prompt` and the image-tool skills.
- **"Post it now"** → this skill renders. Publishing goes through `scheduling-and-queue` with
  confirmation.

## Related skills

- `carousel-strategy` — goal, content type and visual format before any copy.
- `carousel-writer`, `hook-writer` — the copy and the cover hook.
- `occasion-posts` — holidays, awareness and remembrance days.
- `design-and-templates`, `brand-profile` — the wider visual system and identity.
- `canva` — template route for teams already in Canva.
- `infographic-and-data-viz`, `quote-cards-and-text-graphics` — single-image siblings.
- `caption-writer`, `scheduling-and-queue` — what happens after the files exist.

## References

- `references/scope-and-connections.md` — what this does and does not do; sibling routing.
- `references/carousel-design-2026-reality.md` — platform specs and what pro carousels look like now.
- `references/the-build-framework.md` — BUILD, the brand-kit fields, fonts, the QA checks and fixes.
- `references/themes-and-recipes.md` — the spec format, theme guide, recipes by goal.
