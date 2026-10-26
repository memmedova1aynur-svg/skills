# Scope, distinctions + connections

carousel-strategy is the **editor's step**: it decides the goal, the content type and the
visual format for each topic, edits topic lists, and, when asked, writes the full carousel.

## Honest scope (never violate)

- **The agent** edits topics, decides goal / type / format, writes copy and visual notes, and
  writes the `carousel-builder` spec. **carousel-builder** renders.
- **It never invents** events, stories, reviews, quotes, dialogues or results, and never
  presents an example situation as real.
- **It makes no unsupported performance claims.** Goal → type pairs are hypotheses to test.
- **It does not schedule or publish.** `scheduling-and-queue` does, on confirmation.

## Distinct from its siblings

- **carousel-strategy (this)**: which carousel to make and why; topic-list editing; the plan
  and, on request, the full copy.
- **carousel-writer**: slide-level copy craft once the structure is chosen.
- **carousel-builder**: rendering, themes, slide types, QA.
- **occasion-posts**: posts tied to a specific day.
- **content-calendar** / **content-pillars**: spreading topics over time and themes.
- **storytelling-and-narrative**: story craft beyond carousels.

## Where this connects

```
brand-profile + audience-research ──► carousel-strategy (FIT: goal → type → format)
                                             │
                     topic plan ◄────────────┤
                                             │ full carousel requested
                     carousel-writer (copy craft) ──► carousel.json ──► carousel-builder
                                                                          │
                                       caption-writer ◄───────────────────┤
                                       scheduling-and-queue (confirmed) ◄─┘
```
