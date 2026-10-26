# The BUILD framework

Five steps from copy to files. Each one has a single owner and a single output.

| | Step | Output |
|---|---|---|
| **B** | Brand kit, once per client | `brands/<client>.json` |
| **U** | Use the copy, map it to slide types | `carousel.json` |
| **I** | Identify the theme (`--theme all` once per series) | `"theme"` in the spec |
| **L** | Launch the build | PNGs, PDF, contact sheet |
| **D** | Debug with QA, then hand off | exit code 0 and a looked-at contact sheet |

## B — The brand kit

```json
{
  "name": "Aynur Məmmədova",
  "handle": "@aynur.smm",
  "language": "az",
  "logo": "logo.png",
  "colors": {
    "bg": "#F7F5F0", "surface": "#FFFFFF", "text": "#16181D",
    "muted": "#5B616B", "accent": "#E8462E"
  },
  "fonts": { "heading": "Montserrat", "body": "Inter" }
}
```

| field | notes |
|---|---|
| `name` | shown in the `tweet` theme header |
| `handle` | footer of every slide and the CTA; `@` is added if missing |
| `language` | `az`, `en`, `ru`, `tr`: swipe/save labels and correct uppercase (`i` → `İ`) |
| `logo` | path relative to the kit; PNG or SVG with a transparent background; optional |
| `byline` | `"line"` replaces the avatar badge at the top with a signature line, `NAME ——— RUBRIC` (uppercase, accent rubric). The rubric comes from the spec's top-level `"rubric"`; omit it for the name and rule alone |
| `colors.bg` | slide background. Light neutrals read as premium |
| `colors.surface` | cards and list rows; usually white or a step off `bg` |
| `colors.text` | near-black, not pure black. The `data` theme uses it as the background |
| `colors.muted` | secondary text; must still pass 4.5:1 on `bg` |
| `colors.accent` | the one brand colour: highlights, bars, buttons |
| `colors.accentInk` | text on accent; computed automatically (white or near-black) if omitted |
| `fonts.heading` / `fonts.body` | Google Fonts family names; override the theme's pair |
| `fonts.display` / `fonts.mono` | optional: serif for `editorial`, mono for `data` |
| `fonts.files` | local font files: `[{ "family", "src", "weight", "style" }]` for brand or licensed fonts |

**Colour rule of thumb:** one accent. If the brand has two, put the second in `surface`, not
in a second accent.

### Fonts that cover Azerbaijani, Turkish and Cyrillic

Tested with this build's glyph check (verify-quarterly; Google Fonts updates coverage):

- **Azerbaijani + Cyrillic:** Inter, Montserrat, Onest, Roboto, Nunito, Raleway, Unbounded
  (sans); Playfair Display, Source Serif 4, Lora (serif); JetBrains Mono, IBM Plex Mono (mono).
- **Azerbaijani, no Cyrillic:** Plus Jakarta Sans, DM Sans, Poppins, Work Sans, Space Grotesk,
  Fraunces.
- **Missing `ə` (fail for Azerbaijani):** Manrope (no capital `Ə`), Rubik, PT Serif, Outfit,
  Figtree, Golos Text.

Many display fonts (Bebas Neue, several "trendy" grotesques) lack `ə`. The build fails with
**missing-glyph** rather than ship a mixed-font word.

## U — Mapping copy to slide types

Take `carousel-writer` output and map each beat:

- Hook → `cover` (title ≤ 6 words, promise in `subtitle`).
- The stake or one idea → `text`.
- Steps, tips, a framework → `list` (or one `text` per step when each needs a sentence).
- A number → `stat`, always with `source`.
- Myth vs fact, before vs after, don't vs do → `compare`.
- A line worth sending → `quote`.
- The summary → `recap` (the screenshot slide).
- The one ask → `cta`.

Use `**word**` for one highlight per slide at most. Highlights everywhere means none anywhere.

## L — Running the build

```
node scripts/build-carousel.cjs <spec.json> [--brand kit.json] [--theme name|all]
                                [--size portrait|square|WxH] [--out dir] [--no-pdf]
node scripts/build-carousel.cjs --init <dir>     scaffold a spec + brand kit
node scripts/build-carousel.cjs --themes         list themes
```

`--brand` overrides the spec's `brand`, so one spec can render for several clients.

## D — The QA checks and how to fix them

| code | level | what it means | fix |
|---|---|---|---|
| `overflow` | error | text does not fit even at 62% size | cut words or split the slide |
| **missing-glyph** | error | the font lacks a letter in the text | choose a covering font |
| **font-missing** | error | the font did not load at all | check the family name; add `fonts.files` offline |
| `contrast` | error | below WCAG AA (3:1 large, 4.5:1 small) | darken `text`/`muted` or change `accent` |
| **safe-zone** | error / warn | text within 64px of an edge (120px at the cover's sides) | shorten; never reduce margins |
| **image-broken** | error | an image file failed to load | fix the path or the file |
| **too-many-slides** | error | over the platform cap | cut |
| `shrunk` | info / warn | auto-fit reduced the type (warn below 80%) | fine at info; cut words at warn |
| **small-type** | warn | text under 26px | fewer words |
| **cover-wordy** | warn | cover title over 8 words | a sharper hook via `hook-writer` |
| **title-wordy** / **wall-of-text** | warn | headline over 10 words / body over 30 | split |
| **unsourced-stat** | warn | a number with no source | add the source or drop the slide |
| **long-list** | warn | more than 6 items | split into two slides |
| **no-cover** / **short-carousel** / **long-carousel** | warn | structure | revisit with `carousel-writer` |
| **no-cta** | info | last slide is not a CTA | usually add one |
| **font-fetch** | warn | Google Fonts unreachable for a family | add `fonts.files` or go online |
| **tone-type** / **tone-motif** / **tone-cta** | error | a slide type, motif or ask that breaks the day's tone | remove it; remembrance days take no selling, jokes or confetti |
| **tone-accent** | warn | accent slide on a remembrance or religious day | drop `"accent"` |
| **long-table** | warn | more than 7 table rows | split the table |

Then open `contact-sheet.png`. Ask: does the cover read at that size? Does the eye know where
to go on every slide? Is there one highlight per slide, not five?
