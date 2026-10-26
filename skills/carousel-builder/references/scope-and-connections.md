# Scope, distinctions + connections

carousel-builder **renders** a carousel: it takes finished slide copy plus a brand kit and
produces upload-ready files (PNGs, PDF, contact sheet) with an automatic QA gate. It is the
production step between the copy and the scheduler.

## Honest scope (never violate)

- **The agent** writes the slide spec (`carousel.json`), maintains the brand kit, picks the
  theme, runs the build and reads the QA. The **script renders** the files locally with
  Playwright + Chromium. No design tool, no paid API.
- **It does not write the copy from scratch.** Thin or missing copy goes to `carousel-writer`
  first; the cover hook to `hook-writer`.
- **It does not generate images.** An `image` slide takes a file the user has (photo,
  screenshot, product shot). Generation lives in `image-prompt` and the image-tool skills.
- **It does not publish.** Finished files go to `scheduling-and-queue`; the scheduling bridge
  publishes them only after explicit user confirmation.
- **QA catches mechanics, not taste.** Overflow, contrast, glyphs, edges, word counts and
  unsourced stats are checked. Whether the idea is good is not; look at the contact sheet.
- **Never fabricate.** A `stat` slide without a source is a warning the agent must resolve with
  the user, not paper over.

## Distinct from its siblings

- **carousel-builder (this)**: copy → finished slide files, one command, on-brand, QA'd.
- **carousel-writer**: the carousel **copy and narrative** (cover, spine, one idea per slide,
  CTA). Its output is this skill's input.
- **design-and-templates**: the reusable **visual system across asset types** (brand kit,
  template set, tool choice). This skill is one concrete, code-rendered template set for one
  asset type; its brand kit can be filled from that system's tokens.
- **canva**: the template route inside Canva. Use it when the team lives in Canva or needs
  in-browser hand editing. Same brand values, different renderer.
- **quote-cards-and-text-graphics**, **infographic-and-data-viz**: single-image graphics.
- **thumbnail-design**, **pinterest-pin-design**: other single asset types.

## Where this connects

```
brand-profile ──► brand kit (brands/<client>.json)
                          │
idea ──► carousel-writer ──► carousel.json ──► carousel-builder ──► PNG / PDF / QA
         (hook-writer)                                             │
                                          caption-writer ◄─────────┤
                                     scheduling-and-queue ◄────────┘ (confirmed by the user)
```

- `brand-profile`: source of colours, fonts and voice for the kit.
- `carousel-writer`, `hook-writer`: the copy and the cover.
- `caption-writer`: the caption and the cover's alt text.
- `linkedin-post-writer`: the post text for a PDF document carousel.
- `scheduling-and-queue`: queue the finished files.
- `analytics-and-reporting`: read results after posting (saves, shares) to decide which theme
  and structure to repeat.
