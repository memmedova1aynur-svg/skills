# Themes and recipes

## The spec format

```json
{
  "title": "Instagram profilini 5 addımda gücləndir",
  "brand": "brands/aynur.json",
  "theme": "minimal",
  "size": "portrait",
  "autoNumber": false,
  "slides": [
    { "type": "cover", "kicker": "SMM bələdçisi", "title": "Profilin **satmır?**", "subtitle": "5 düzəliş, bu gün 20 dəqiqəyə." },
    { "type": "text", "title": "Bio nə etdiyini deməlidir", "body": "**Kimə** və **nə** ilə kömək etdiyini bir cümlədə yaz." },
    { "type": "cta", "title": "Yadda saxla, sabah yoxla.", "action": "Yadda saxla" }
  ]
}
```

- `brand`: a path (relative to the spec) or an inline object. `--brand` overrides it.
- `theme`: one of the six; `--theme` overrides it.
- `size`: `portrait` (1080x1350), `square` (1080x1080), `linkedin`, or `WxH`.
- `autoNumber`: numbers `text` and `list` slides 01, 02, … (on by default in `steps`).
- Any slide: `"accent": true` for an accent-background beat; `"number": "03"` to set a number.
- Cover: `"image": "photo.jpg"` for a full-bleed photo under a dark gradient (text turns white).
  Use a real photo of the person, product or place; it outperforms stock.
- CTA: `"icon"`: `save` (default), `share`, `comment`, `follow` or `link`, matching the one ask.
- Text: `**word**` for accent highlight, `\n` for a line break.

A full eight-slide Azerbaijani example is in `assets/examples/example-carousel.json`.

## The six themes

Built into every theme (each tunes or hides them): author badge + page counter, a continuous
line across slide edges, oversized faint slide numbers, grain, card shadows, swipe button, SVG
icons, CTA profile card.

| theme | looks like | best for | avoid for |
|---|---|---|---|
| `minimal` | off-white, accent bar, generous air | experts, services, premium brands | loud promos |
| `bold` | uppercase heavy type, accent cover/CTA, marker highlights | hot takes, myths, lists | long sentences |
| `editorial` | serif display, rules, italic highlights | essays, stories, opinion | dense data |
| `tweet` | avatar + name + handle, post-card text | founders, personal brands, opinions | product catalogues |
| `data` | dark grid, huge accent numbers, mono labels | stats, research, results | soft lifestyle brands |
| `steps` | progress rail, giant outlined numbers | how-tos, checklists, processes | stories |

Pick by content, then **keep the theme for the series**. Rotating themes every post throws away
the recognition a system buys.

## Recipes by goal

**Saves (teach): "N steps"**, theme `steps` or `minimal`
cover → text (the stake) → text × N (one step each) → recap → cta (save)

**Shares (opinion): "Myth vs fact"**, theme `bold` or `tweet`
cover → compare × 3 → quote (the line to send) → cta (send to a friend)

**Authority (results): "Case study"**, theme `data` or `editorial`
cover → text (the situation) → stat × 2-3 (with sources) → list (what we did) → recap → cta

**Leads (offer): "Problem → fix"**, theme `minimal`
cover → text (the pain) → list (why it happens) → compare (old vs new way) → text (the offer, one
line) → cta (comment a keyword; DM flow via the DM skills)

**Personal story**, theme `editorial` or `tweet`
cover → text × 4-6 (one beat each) → quote (the lesson) → cta (follow)

## Working fast across clients

```
clients/
  brands/   aynur.json  cafe-baku.json  dental-plus.json
  aynur/    2026-11-03-bio.json  2026-11-05-hooks.json
  cafe-baku/2026-11-04-menu.json
```

One spec can render for another client with `--brand brands/cafe-baku.json`. For a batch, loop
over the specs; each build is about two seconds per theme once fonts are cached.
