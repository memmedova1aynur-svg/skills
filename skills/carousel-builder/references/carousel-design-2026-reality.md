# Carousel design: 2026 reality

> Platform specs move. Numbers here are tagged **verify-quarterly**; the design principles are
> durable. Never quote a reach or save-rate figure you cannot source.

## Specs the build defaults to

| | Instagram | LinkedIn document | TikTok photo |
|---|---|---|---|
| Size | 1080x1350 (4:5), or 1080x1080 | PDF; portrait or square | 9:16 vertical |
| Slides | up to 20 (verify-quarterly) | generous; keep it tight | varies |
| Build flag | `--size portrait` (default) | use `carousel.pdf` | `--size 1080x1920` |

- **Keep every slide the same ratio.** Instagram crops the rest of the post to the first
  slide's ratio.
- **The profile grid crops the cover.** The grid thumbnail is narrower than a 4:5 post and the
  exact ratio has changed more than once (verify-quarterly). The build keeps cover text 128px
  from the sides and warns inside 120px, so the crop stops mattering.
- **Exported PNGs are exactly the target size** (device scale 1). Upload them as they are;
  re-saving through a phone gallery app can recompress text edges.

## What professional carousels look like now

Look at accounts that grow on carousels in any niche and the pattern is the same:

- **Big type, few words.** Headlines read from arm's length. A slide is a billboard, not a page.
- **One system across the whole carousel and the whole series.** Same margins, same type
  scale, same footer. Followers recognise the post before they read the name.
- **A footer with the handle on every slide.** Screenshots travel without the caption.
- **Visible progress.** Page numbers or a progress rail lift completion; people swipe to an end
  they can see.
- **A recap slide built to be screenshotted and sent.** Sends are a strong signal.
- **Native beats glossy.** The text-post look (`tweet` theme) and plain editorial layouts often
  outperform stock-photo-heavy designs because they read as a person talking.
- **Restraint with colour.** Neutral background, one accent, used for emphasis only.
- **Seamless edges.** A line or shape that crosses from one slide into the next tells the eye
  there is more and makes the carousel feel like one designed object.
- **A face or a name up top.** An author badge turns a graphic into a person talking, and keeps
  credit on screenshots.
- **Texture and depth, lightly.** Subtle grain and soft card shadows read as print and polish;
  heavy drop shadows and glows read as template.

## What makes carousels look amateur

- Text touching the edges; mixed margins from slide to slide.
- Three fonts, five colours, drop shadows on text.
- Paragraphs on slides; 24px body text.
- A font that silently swaps `ə` or `ğ` to a fallback glyph mid-word (common with display
  fonts and Latin-only fonts). The build fails on this.
- Low-contrast "aesthetic" palettes: beige on cream, grey on grey.
- Unsourced statistics in huge type.

## Accessibility is part of "professional"

- Contrast: the build uses WCAG AA, 3:1 for large text and 4.5:1 for small text.
- Alt text: write it for the cover at minimum (handled with the caption by `caption-writer`).
- Don't encode meaning in colour alone; the `compare` slide pairs colour with labels.
