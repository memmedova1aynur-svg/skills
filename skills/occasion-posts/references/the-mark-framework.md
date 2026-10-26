# The MARK framework

| | Step | Output |
|---|---|---|
| **M** | Match the day | an occasion id from the calendar, date verified |
| **A** | Assign the tone | `"tone"` in the spec; palette and allowed slide types follow |
| **R** | Render the visual | photo, AI image or motif; spec scaffolded and filled |
| **K** | Keep it right | renderer QA 0, avoid list cleared, facts sourced, user confirms |

## The calendar (`assets/calendar.json`)

Generated from `scripts/make-calendar.py`; edit the Python and re-run, never the JSON by hand.

| field | meaning |
|---|---|
| `id` | stable key for the scripts |
| `name.az` / `name.en` | display names |
| `date` | `"MM-DD"`, or `null` for movable days |
| `rule`, `approx_month` | how a movable date is set; which month to watch |
| `verify` | true when the date or theme must be checked each year |
| `tone` | celebration, awareness, religious or remembrance |
| `groups` | az-national, child-development, international |
| `niches` | e.g. speech, education, inclusion, dental, cafe, psychology, health, fitness, travel |
| `motifs` | motif-library names that fit, best first |
| `palette` | a key into `palettes` (colours for the day) |
| `angles` | content angles that work |
| `avoid` | what not to do on this day |
| `ai_prompt` | base prompt for an image tool (no text in image) |
| `note` | clashes and cautions |
| `scope` | Azərbaycan, beynəlxalq, or both |
| `status` | official (declared by a state or UN-system body) or unofficial |
| `source` | the declaring authority; open its page before first use |
| `source_verified` | false until a person has checked the source link |
| `formats` | formats that fit the tone |

Days with no `niches` and group az-national always show in `upcoming.cjs`, whatever the niche
filter: every Azerbaijani audience notices them.

## Scripts

```
node scripts/upcoming.cjs [--days 45] [--from YYYY-MM-DD] [--niche a,b] [--group az-national]
node scripts/upcoming.cjs --show <id>
node scripts/upcoming.cjs --spec <id> [--format post|carousel] [--brand kit.json] [--out file.json]
```

Prepare-by dates: remembrance 3 days, religious 5, awareness and celebration 7. Big campaigns
(New Year, Novruz sales) need weeks; plan those in `seasonal-and-moment-marketing`.

## Adding a niche or a day

Add a `d(...)` line to `make-calendar.py` with a real date or a rule, the tone, motifs from the
library, angles and an avoid list. Mark anything you are not sure of with `verify=True`. Run
the script and check `upcoming.cjs` lists it.
