# Copy rules and output templates

## Copy rules

- Natural, professional Azerbaijani (or the user's language). Short sentences, full content.
- One main idea per slide.
- Complete general advice with a concrete example or application.
- A number in the title is optional, never mandatory.
- Speak to the audience's profession and real difficulty directly.
- No long introduction or motivational preamble unless the topic needs it.
- Don't restate an idea in other words to fill a slide.
- Vary the ending; don't close every carousel with the same ask.
- Check claims on child development, education, psychology and health against reliable
  sources (WHO, UNICEF, national health and education authorities, peer-reviewed reviews).

### Banned patterns

- Artificial curiosity: "Şok olacaqsınız", "Heç kim bunu demir", "Uğurun sirri", "Bunu
  bilmədən…", "son slayda qədər oxuyun".
- Repeated constructions: "X kifayət etmir", "Bu sadəcə X deyil, Y-dir" used again and again.
- Empty instructions left in finished copy: "burada izah et", "nümunə əlavə et".
- Unsupported performance promises: "bu növ hər zaman ən çox baxış yığır".

## Mode A template — edited topic list

```
REDAKTƏ QEYDLƏRİ
- Birləşdirildi: "…" + "…" → "…" (eyni fikir)
- Konkretləşdirildi: "…" → "…"
- Ayrıldı: "…" — səbəb: …

1. Başlıq: …
   Məqsəd: …
   Karusel növü: … (+ köməkçi: …)
   Vizual format: …
   Oxucunun faydası: … (nəyi anlayacaq / yoxlayacaq / tətbiq edəcək)
```

## Mode B template — full carousel

```
Başlıq · Məqsəd · Növ (+ köməkçi) · Vizual format · Fayda

SLAYD 1 — [cover]
Mətn: …
Vizual: …

SLAYD 2 — [slide type]
Mətn: …
Vizual: …
…

YEKUN / ÇAĞIRIŞ: …   (mövzuya uyğun; həmişə eyni deyil)
CAPTION: 2-4 qısa cümlə, təbii; ilk sətir kəsilmədən əvvəl dəyəri desin.
MƏNBƏ: … (iddia varsa)
```

Then convert to a `carousel-builder` spec: one JSON slide per slide above, the slide type
named in brackets, the visual note turned into `motif`, `image`, `theme` or `accent` choices.
Render and check the QA before showing it.
