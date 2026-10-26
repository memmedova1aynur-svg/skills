# Recipes and prompts

## Recipes by tone

**Greeting post (celebration, religious):** one `greeting` slide, `format: "post"`.
Motif or photo, kicker = the day, title = the greeting, message = one or two sincere lines
tied to the brand's audience, signature = brand or person. Example: `assets/examples/novruz-post.json`.

**Remembrance post:** one `greeting` slide, `tone: "remembrance"`, `format: "post"`, motif
`qerenfil` or `sam`, kicker = date and year, title = official name of the day, message = one
sentence of remembrance, signature = "Allah rəhmət eləsin" or the brand name. No CTA.
Example: `assets/examples/20-yanvar-post.json`.

**Awareness carousel:** cover with the day as kicker → 3-4 `compare` myth/fact or `text`
slides → `recap` (what to do) → `cta` (share, not save-and-sell) with the source named.
Example: `assets/examples/autizm-karusel.json`.

**Celebration carousel with practice:** cover (day + practical promise) → `list` or `table`
(e.g. Novruz with children: 5 activities) → `greeting` → `cta`. Add `"ornament": "konfetti"`
for New Year and 1 June only.

**Offer on a celebration day:** greeting first, then a `poster` slide with the offer. Never
the poster alone on the day itself.

## AI image prompts: rules

- Start from the calendar's `ai_prompt`; add the brand's palette and the slide's crop
  (portrait 4:5, subject in the upper half for a cover with text below).
- **No text in the image.** All words go in the renderer; image models misspell ə, ğ, ı.
- Name the culture precisely ("Azerbaijani Novruz khoncha with semeni and shekerbura") and
  name what it is NOT ("not Persian haft-sin, no goldfish bowl").
- No identifiable children's faces; hands, backs, objects instead.
- No realistic images of tragedies, war or victims. Remembrance uses motifs or real archive
  photos from an official source with credit.
- Check every result against the day's `avoid` list; regenerate rather than "close enough".

## Prompt bases (extend per brand)

| day | base prompt |
|---|---|
| Novruz | Azerbaijani Novruz khoncha: copper tray, green semeni with red ribbon, shekerbura, pakhlava, gogal, dyed eggs, candles, warm daylight, top-down, no text; not Persian haft-sin |
| Yeni il | festive still life, decorated fir branch, warm string lights, gold and deep green, soft bokeh, no text |
| 1 iyun | joyful flat illustration of balloons, kites and building blocks in a sunny park, no text, no faces |
| 2 aprel | child and parent hands building with colourful wooden blocks, calm light, gentle rainbow accents, no puzzle pieces, no text |
| Bilik günü | school backpack, notebooks and coloured pencils on a light desk, morning light, no text, no faces |
| 8 Mart | bouquet of red tulips on a soft pink background, natural light, minimal, no text |
