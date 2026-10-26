---
name: carousel-strategy
description: >-
  The editor's step before a carousel is written: fix one goal, pick the content type (21
  types, explainer to scenario test) plus an optional helper, choose the visual format, then
  write. Use when the user sends a topic or a topic list for experts, teachers,
  trainers, mentors or businesses, says "which carousel type," "edit my topic list," "plan
  carousels for this page," "mövzuları redaktə et," "karusel növü," "storytelling karusel,"
  or wants carousels that don't repeat across clients. Edits topic lists (merge duplicates,
  sharpen vague topics, drop misfits with a reason) and returns title, goal, type, visual
  format and reader benefit per topic; on request writes the full carousel: slide copy, a
  visual note per slide, ending, caption, and a carousel-builder spec. Strict storytelling and
  honesty rules: no invented events, quotes, reviews or results. Uses the FIT framework.
  Hands slide copy craft to carousel-writer and rendering to carousel-builder.
metadata:
  version: 1.0.0
license: MIT
---

# Carousel Strategy

A topic split into slides is not a carousel. A carousel is a decision: **what should the
reader be able to understand, check or do afterwards**, and which structure gets them there.
This skill makes that decision explicitly for every topic, so a page run for a teacher, a
trainer and a café never ends up with the same ten carousels in different colours.

The quality test for every output: **after the last slide, what will the reader concretely
understand, check or apply?** If the answer is vague, the plan is not done.

Default output language is the user's language (Azerbaijani for this workspace): natural,
professional, short sentences.

## Step 0 — Read the page

Load the client's brand profile, audience and past topics if they exist (`brand-profile`,
`audience-research`, `content-pillars`). Note the profession of the audience, their real daily
problems, and which types and formats the page used recently: the plan should vary them.

## Step 1 — F: Fix one goal

Each carousel has **one** main goal. They are different results and are not interchangeable:

views and reach · saves · shares · comments and discussion · expertise and trust ·
profile visits · applications to a service or programme.

## Step 2 — I: Identify the content type

Choose from the 21 types in `references/the-fit-framework.md` (explainer, step-by-step,
list, checklist, problem–solution, mistakes and fixes, myth–reality, comparison,
before–after, case study, storytelling, expert position, ready tool/template, resource
collection, Q&A, test/scenario, behind the scenes, reviews and participant experience,
service/programme presentation, photo story, humour/familiar situations).

Combine one main type with one helper when the topic needs it: storytelling + practical
takeaway, case study + checklist, comparison + template, problem–solution + steps.

Goal → type are **working hypotheses to test**, not a ranking (see
`references/carousel-performance-2026-reality.md`):
- views and shares: familiar problems, strong stories, before–after, argued expert position
- saves: step-by-step, checklist, template, resource collection
- discussion: scenario test, choice, comparison, expert position
- trust: case study, annotated material, process
- applications: programme presentation, real results, Q&A

## Step 3 — T: Treat it visually

Choose the visual format separately from the content type: typographic, editorial, infographic,
photo + explanation, card system, annotated example, continuous panorama, collage, dialogue or
comic, mixed media, photo story. The format must make the information easier to grasp, not
just look good. Keep the client's palette, fonts and rules. Each format maps to
`carousel-builder` themes and slide types (table in `references/the-fit-framework.md`).

## Mode A — The user sends topics

1. **Edit the list first:** merge duplicates and near-duplicates (the same idea in other
   words is one topic), make vague topics specific, set aside topics that don't fit the
   audience with a one-line reason, and keep strong titles as they are.
2. **Then, per topic:** edited title · main goal · content type (+ helper) · visual format ·
   the concrete benefit for the reader.

Template: `references/copy-rules-and-templates.md`.

## Mode B — The user asks for the full carousel

Add to the plan: slide-by-slide copy ready to post, a short visual note per slide, an ending
or call to action that fits the topic (not the same ask every time), and a short natural
caption. Choose the slide count by the content; never pad. No placeholders like "explain here"
in finished copy. Then write the `carousel-builder` spec (`carousel.json`) and render it.

For storytelling, follow `references/storytelling-rules.md` strictly: a concrete situation, the
goal or expectation, the obstacle, the decision, the result, and what the reader can take away.

## Honesty rules (never break)

- No invented events, client stories, reviews, dialogues, quotes or results. If a real story
  lacks details, ask only for the missing ones.
- A typical situation that did not happen is labelled **"nümunə situasiya"** (example situation).
- No quotation marks around sentences nobody said.
- An observation is not presented as proven cause and effect.
- Claims on child development, education, psychology and health are checked against reliable
  sources; the source is named on the slide or in the caption.
- No unsupported performance claims ("this type always gets the most views").

## Quality bar — self-check

- One goal, named? Type and format chosen for that goal, not by habit?
- Topic list: duplicates merged, vague topics sharpened, misfits explained?
- Every slide adds a new fact, detail or meaning? No repeated idea in new words?
- No clickbait ("şok olacaqsınız", "heç kim bunu demir", "uğurun sirri"), no overused
  "not X, but Y" patterns, no long motivational intro?
- The practical answer is not hidden until the end for no reason?
- The ending fits this topic, and differs from the page's last few carousels?
- Can you state what the reader will understand, check or apply?

## Related skills

- `carousel-writer` — slide-level copy craft; `hook-writer` — the cover line.
- `carousel-builder` — renders the spec (themes, slide types, QA).
- `occasion-posts` — day-specific posts; `storytelling-and-narrative` — story craft in depth.
- `educational-content-and-how-to`, `social-proof-and-testimonials`,
  `before-after-and-transformation`, `meme-and-culture` — deeper guides for single types.
- `caption-writer` — the caption; `content-calendar` — spreading types across the month.

## References

- `references/scope-and-connections.md` — what this skill owns and hands off.
- `references/carousel-performance-2026-reality.md` — what the data does and does not say.
- `references/the-fit-framework.md` — goals, the 21 types, combinations, visual formats, renderer mapping.
- `references/storytelling-rules.md` — story types A–H, the flexible flow, title directions, rules.
- `references/copy-rules-and-templates.md` — copy rules, banned patterns, output templates.
