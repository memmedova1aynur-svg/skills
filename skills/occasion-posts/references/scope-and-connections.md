# Scope, distinctions + connections

occasion-posts makes **day-specific** posts and carousels: it knows the day, its tone, its
symbols and its pitfalls, and turns that into a spec `carousel-builder` renders.

## Honest scope (never violate)

- **The agent** matches the day, assigns the tone, chooses the image source, writes the copy
  and checks the result. The **calendar** (`assets/calendar.json`) supplies tone, palette,
  motifs, angles, avoid lists and AI prompts. **carousel-builder** renders and enforces tone.
- **It does not decide whether a brand should join a day.** That gate is
  `seasonal-and-moment-marketing`.
- **It does not generate images itself.** It provides checked prompts; a connected image tool
  generates (routed through `image-prompt`). The motif library is the no-tool fallback.
- **It never invents a movable date** (Novruz, çərşənbələr, Ramazan, Qurban, Mother's Day) or
  a historical fact or number. Those are verified each year from official sources.
- **It does not schedule or publish.** `scheduling-and-queue` does, with user confirmation.

## Distinct from its siblings

- **seasonal-and-moment-marketing**: the annual plan and the fit gate. This skill executes
  one day well.
- **carousel-builder**: the renderer, motif library and tone QA.
- **carousel-writer** / **carousel-strategy**: structure and copy for the carousel itself.
- **trend-jacking**: reactive moments with no fixed date.
- **image-prompt** and the image-tool skills: generation.

## Where this connects

```
seasonal-and-moment-marketing ──► which days ──► upcoming.cjs (MATCH)
                                                     │
                                       tone + palette + motif (ASSIGN)
                                                     │
            photo │ image-prompt → image tool │ motif library (RENDER)
                                                     │
                                carousel-builder (tone QA) ──► caption-writer
                                                     │
                                       scheduling-and-queue (confirmed)
```
