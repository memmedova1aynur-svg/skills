# Writing and Publishing Essentials

Everything the remake needs to be written and posted well, in one place. Platform numbers are
**verify-quarterly**: they move.

## The hook (first 3 seconds)

The hook is three things that land together: the **first frame**, the **first spoken line**
and the **first on-screen line**. Most outliers stack at least two.

Rules:

1. **Open a loop in under 2 seconds.** A conflict ("My client tried this on me"), a promise
   ("3 things nobody tells you about…"), a surprising claim, or a visual that needs explaining.
2. **No warm-up.** Cut "Hey guys," "So today," logos and intros. Start mid-sentence if needed.
3. **The on-screen line adds, it doesn't repeat.** Spoken: "My landlord tried this." Text: "he
   didn't expect #3."
4. **Specific beats general.** "Rent up 18% on two weeks' notice" beats "rent is going up."
5. **Match the source's hook type, not its words.** If the source used conflict + promise, the
   remake uses a conflict + promise from the user's world.

Always give 3 alternative hooks with the remake, each a different type (conflict, promise,
claim), so the user can film two takes and pick.

## On-screen text

- 3 to 7 words per card, readable in under a second.
- Appears 0.1 to 0.3 seconds after the cut, so the eye lands first.
- Most people watch with the sound off: burned-in captions (2 to 4 words per line) plus the
  on-screen text cards carry the whole story without audio.
- Keep everything inside the safe zone (below).

## The caption

1. **First line = the keyword + the reason to watch.** Instagram and TikTok are searched like
   search engines; say what it's about in the words people type ("freelance contract revision
   clause").
2. **One to three short lines of value or context** the video didn't have room for.
3. **One question that invites a real answer** (a story, an opinion), not "thoughts?"
4. **3 to 5 specific hashtags** at most, or none; broad tags like #viral do nothing.
5. In the user's voice; no promises they can't back up.

## The cover

- Chosen **before** publishing; on Instagram it **can't be changed after**.
- A custom image beats a random video frame: the hook frame with the hook text, bold and large
  (at least ~60px at 1080 width), centered.
- Instagram shows it 9:16 in the Reels tab but crops it to **3:4 (1080x1440)** on the profile
  grid, so keep the face and text in the center.

## Audio

- Never reuse the source's audio or voice.
- For a trending sound: add it **in the app** from the platform's own library (licensed there),
  quietly under the voice. On TikTok that's why the post goes up as a draft.
- For an original sound: the user's voice plus room tone is fine; many outliers are just a voice.
- If the user wants made music, it must be music they have commercial rights to.

## Video specs and safe zone

| | Instagram Reel | TikTok | YouTube Short |
|---|---|---|---|
| Aspect / size | 9:16, 1080x1920 | 9:16, 1080x1920 | 9:16, 1080x1920 |
| Length | up to 3 min in-app (verify) | per account; check `maxVideoPostDurationSec` in WoopSocial's platform inputs | up to 3 min (verify) |
| Safe zone | keep text and faces out of the top ~250px and bottom ~350px | similar; bottom ~350px and right edge carry buttons | similar; bottom ~350px |
| Watermarks | remove other platforms' watermarks | same | same |

Export H.264 MP4, 30fps, at a high bitrate (around 15 to 20 Mbps) so the platform's compression
doesn't blur text.

## Publish settings per platform

**Instagram Reel** (via WoopSocial, see `woopsocial.md`)

- Post type **REEL** + the video + the caption + the cover image.
- Done in the app, not via API: picking a trending sound, Share-to-Feed tweaks, collaborator and
  product tags. Tell the user if they want any of these.

**TikTok**

- Upload with mode **`MEDIA_UPLOAD`**: it lands in the user's TikTok drafts/inbox. They add the
  trending sound in the app and post. Use **`DIRECT_POST`** only when no in-app sound is wanted.
- Privacy level: one of the values WoopSocial's platform inputs return for that account.
- Leave comments, duets and stitches **on** (they're reach) unless there's a brand-safety reason.
- Disclosure: branded content and paid partnerships must be marked truthfully. If the remake
  uses AI-generated footage or voice, WoopSocial applies TikTok's AI label automatically.

**YouTube Shorts**

- Same file; give it its own title (keyword first, under ~60 characters) and a short
  description.

## The confirmation (always)

Before publishing, show the user exactly what will go out:

```
Instagram  REEL  | remake-final.mp4 | cover.jpg | Thu 2026-10-22 18:30
Caption:   <full caption>
TikTok     MEDIA_UPLOAD (drafts, add sound in-app) | <caption>
Post these? (yes / change something)
```

Publish only after an explicit yes. A "looks good" about the script is not a yes to publish.
