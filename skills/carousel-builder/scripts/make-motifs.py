#!/usr/bin/env python3
"""Generate the motif illustration library (assets/motifs/*.svg + motifs.json).

Flat, geometric, one consistent style so motifs mix on a slide. Colours are the motif's real
colours (green səməni, red carnation, the flag's official hues) because occasion imagery that
gets these wrong reads as careless. Deterministic: re-running produces identical files.

    python3 scripts/make-motifs.py
"""
import json, math, os, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'motifs')
os.makedirs(OUT, exist_ok=True)
rng = random.Random(7)
MOTIFS = {}


def save(name, body, uses, tone='celebration'):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{body}</svg>\n'
    open(os.path.join(OUT, f'{name}.svg'), 'w').write(svg)
    MOTIFS[name] = {'uses': uses, 'tone': tone}


def star_points(cx, cy, n, ro, ri, rot=-90):
    pts = []
    for k in range(n * 2):
        r = ro if k % 2 == 0 else ri
        a = math.radians(rot + k * 180 / n)
        pts.append(f'{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}')
    return ' '.join(pts)


# səməni: wheatgrass in a copper dish, red ribbon (Novruz)
blades = []
for k in range(46):
    x0 = 52 + k * 2.1 + rng.uniform(-1.5, 1.5)
    h = rng.uniform(70, 112)
    lean = rng.uniform(-22, 22)
    w = rng.uniform(2.6, 4.2)
    col = rng.choice(['#3F9B4A', '#4FAF57', '#2F8441', '#62BF62'])
    blades.append(f'<path d="M{x0 - w:.1f} 140 Q{x0 + lean * .4:.1f} {140 - h * .55:.1f} {x0 + lean:.1f} {140 - h:.1f} '
                  f'Q{x0 + lean * .4 + w:.1f} {140 - h * .5:.1f} {x0 + w:.1f} 140Z" fill="{col}"/>')
save('semeni', ''.join(blades) +
     '<rect x="46" y="118" width="108" height="12" rx="3" fill="#D7263D"/>'
     '<path d="M100 124 l-14 22 8-1 4 8 4-22z M100 124 l14 22 -8-1 -4 8 -4-22z" fill="#B81E33"/>'
     '<ellipse cx="100" cy="146" rx="62" ry="12" fill="#C9822B"/>'
     '<path d="M40 146 Q100 196 160 146Z" fill="#B5701F"/>'
     '<ellipse cx="100" cy="146" rx="62" ry="12" fill="none" stroke="#E0A350" stroke-width="3"/>',
     ['novruz', 'spring'])

# tonqal: bonfire (Novruz çərşənbələri, od çərşənbəsi)
save('tonqal',
     '<g stroke-linecap="round"><path d="M50 172 L150 146" stroke="#6B3E1F" stroke-width="16"/>'
     '<path d="M50 146 L150 172" stroke="#83502A" stroke-width="16"/></g>'
     '<path d="M100 26 C128 62 150 82 146 118 C143 146 124 160 100 160 C76 160 56 146 54 118 C52 92 70 84 76 60 C86 76 90 82 96 84 C96 62 92 46 100 26Z" fill="#F0592A"/>'
     '<path d="M102 66 C118 90 132 104 128 128 C125 146 114 154 100 154 C86 154 74 146 73 130 C72 112 84 106 88 92 C94 102 98 106 100 106 C102 92 98 80 102 66Z" fill="#F9A03F"/>'
     '<path d="M101 106 C110 120 116 128 114 140 C112 149 107 152 100 152 C93 152 88 148 87 140 C86 130 94 126 96 118 C99 122 100 124 101 124Z" fill="#FFE07A"/>',
     ['novruz', 'od-cersenbe', 'winter'])

# şam: candle with glow (remembrance)
save('sam',
     '<circle cx="100" cy="58" r="40" fill="#FFD27A" opacity=".18"/><circle cx="100" cy="58" r="24" fill="#FFD27A" opacity=".28"/>'
     '<path d="M100 30 C110 46 112 56 108 66 C106 72 103 74 100 74 C97 74 94 72 92 66 C88 56 90 46 100 30Z" fill="#FFB238"/>'
     '<path d="M100 48 C105 56 106 62 104 67 C103 70 101.5 71 100 71 C98.5 71 97 70 96 67 C94 62 95 56 100 48Z" fill="#FFF1B8"/>'
     '<rect x="98.5" y="72" width="3" height="10" fill="#3A2A1A"/>'
     '<rect x="80" y="82" width="40" height="92" rx="6" fill="#F4EFE6"/>'
     '<path d="M80 92 Q88 98 92 90 Q96 104 100 92 V82 H80Z" fill="#E6DFD2"/>'
     '<rect x="112" y="82" width="8" height="92" rx="4" fill="#E2DACB"/>',
     ['remembrance', 'mourning'], tone='remembrance')

# qərənfil: red carnation (Azerbaijani symbol of remembrance)
petals = []
for ring, (r, n, col) in enumerate([(54, 16, '#A10F2B'), (42, 13, '#C8183A'), (30, 10, '#DF2F4D'), (16, 7, '#EF5670')]):
    for k in range(n):
        a = math.radians(k * 360 / n + ring * 11)
        cx, cy = 100 + r * .62 * math.cos(a), 64 + r * .5 * math.sin(a)
        pts = star_points(cx, cy, 6, r * .5, r * .34, rot=math.degrees(a))
        petals.append(f'<polygon points="{pts}" fill="{col}"/>')
save('qerenfil',
     '<path d="M100 100 C97 130 103 160 99 194" stroke="#3C7A3A" stroke-width="6" fill="none" stroke-linecap="round"/>'
     '<path d="M100 152 C82 140 66 142 54 152 C70 158 86 158 100 154Z" fill="#4B8C45"/>'
     '<path d="M100 132 C118 122 134 124 146 132 C130 140 114 140 100 134Z" fill="#4B8C45"/>'
     '<path d="M84 96 L100 116 L116 96 L110 88 L90 88Z" fill="#4B8C45"/>' + ''.join(petals)
     + '<circle cx="100" cy="64" r="9" fill="#EF5670"/>',
     ['remembrance', 'mourning', '8-mart', 'national'], tone='remembrance')

# şarlar: balloons (birthdays, children's day)
def balloon(cx, cy, r, col, hi):
    return (f'<path d="M{cx} {cy + r * 1.18} Q{cx - 6} {cy + r * 1.6} {cx + 4} {cy + r * 2.1} T{cx - 2} {190}" stroke="#9AA0A6" stroke-width="1.6" fill="none"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 1.18}" fill="{col}"/>'
            f'<path d="M{cx - 5} {cy + r * 1.16} l5 7 5-7z" fill="{col}"/>'
            f'<ellipse cx="{cx - r * .38}" cy="{cy - r * .45}" rx="{r * .18}" ry="{r * .3}" fill="{hi}" opacity=".55" transform="rotate(-25 {cx - r * .38} {cy - r * .45})"/>')
save('sarlar', balloon(72, 70, 30, '#F25C54', '#FFFFFF') + balloon(130, 58, 32, '#4CC9F0', '#FFFFFF') + balloon(104, 104, 26, '#FFC43D', '#FFFFFF'),
     ['1-iyun', 'birthday', 'children', 'celebration'])

# yolka: new year tree
save('yolka',
     '<rect x="92" y="160" width="16" height="22" rx="3" fill="#7A4A26"/>'
     '<path d="M100 40 L150 110 H124 L160 160 H40 L76 110 H50Z" fill="#1F7A4D"/>'
     '<path d="M100 40 L150 110 H124 L130 118 H70 L76 110 H50Z" fill="#26915B"/>'
     f'<polygon points="{star_points(100, 36, 5, 14, 6)}" fill="#FFC93C"/>'
     '<circle cx="84" cy="98" r="6" fill="#E63946"/><circle cx="116" cy="124" r="6" fill="#4CC9F0"/>'
     '<circle cx="76" cy="146" r="6" fill="#FFC93C"/><circle cx="128" cy="148" r="6" fill="#E63946"/><circle cx="102" cy="138" r="5" fill="#FFFFFF"/>',
     ['yeni-il', 'winter'])

# qar dənəsi: snowflake
arms = []
for k in range(6):
    a = k * 60
    arms.append(f'<g transform="rotate({a} 100 100)"><path d="M100 100 V30 M100 52 L86 40 M100 52 L114 40 M100 72 L88 62 M100 72 L112 62" '
                'stroke="#7CC6F2" stroke-width="7" stroke-linecap="round" fill="none"/></g>')
save('qar', ''.join(arms) + '<circle cx="100" cy="100" r="9" fill="#7CC6F2"/>', ['yeni-il', 'winter'])

# sonsuzluq: rainbow infinity (neurodiversity / autism acceptance; NOT the puzzle piece)
save('sonsuzluq',
     '<defs><linearGradient id="mo-inf" x1="0" x2="1"><stop offset="0" stop-color="#E63946"/><stop offset=".2" stop-color="#F4A261"/>'
     '<stop offset=".4" stop-color="#F6D743"/><stop offset=".6" stop-color="#4CAF50"/><stop offset=".8" stop-color="#3A86FF"/>'
     '<stop offset="1" stop-color="#8E44AD"/></linearGradient></defs>'
     '<path d="M100 100 C80 62 30 62 30 100 C30 138 80 138 100 100 C120 62 170 62 170 100 C170 138 120 138 100 100Z" '
     'fill="none" stroke="url(#mo-inf)" stroke-width="20" stroke-linejoin="round"/>',
     ['autizm', 'neurodiversity', 'inclusion'], tone='awareness')

# ürək: heart
save('urek', '<path d="M100 170 C40 126 22 96 34 66 C46 38 84 36 100 64 C116 36 154 38 166 66 C178 96 160 126 100 170Z" fill="#E63946"/>'
     '<path d="M58 64 C66 54 80 54 86 62" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" fill="none" opacity=".6"/>',
     ['14-fevral', 'ana-gunu', 'family', 'kindness'])

# kitab: open book (Bilik günü, book day, teachers)
save('kitab',
     '<path d="M100 60 C80 48 52 46 26 52 V152 C52 146 80 148 100 160Z" fill="#3A86FF"/>'
     '<path d="M100 60 C120 48 148 46 174 52 V152 C148 146 120 148 100 160Z" fill="#2667CC"/>'
     '<path d="M100 66 C82 56 58 54 36 58 V144 C58 140 82 142 100 152Z" fill="#FFFFFF"/>'
     '<path d="M100 66 C118 56 142 54 164 58 V144 C142 140 118 142 100 152Z" fill="#F2F4F8"/>'
     + ''.join(f'<path d="M48 {76 + k * 14} C64 {73 + k * 14} 78 {75 + k * 14} 90 {80 + k * 14}" stroke="#C5CBD6" stroke-width="3" fill="none"/>' for k in range(5))
     + ''.join(f'<path d="M110 {80 + k * 14} C122 {75 + k * 14} 136 {73 + k * 14} 152 {76 + k * 14}" stroke="#C5CBD6" stroke-width="3" fill="none"/>' for k in range(5)),
     ['bilik-gunu', 'kitab-gunu', 'muellim', 'education'])

# ulduz: 8-point star (Azerbaijani ornament / national)
save('ulduz', f'<polygon points="{star_points(100, 100, 8, 78, 42)}" fill="#E8B23A"/>'
     f'<polygon points="{star_points(100, 100, 8, 44, 24)}" fill="#F6D37A"/>',
     ['national', 'novruz', 'celebration'])

# bayraq: Azerbaijan flag (1:2; crescent + eight-pointed star in the red band)
save('bayraq',
     '<g transform="translate(0 50)"><rect width="200" height="100" rx="4" fill="#EF3340"/>'
     '<rect width="200" height="33.4" rx="4" fill="#00B5E2"/><rect y="20" width="200" height="13.4" fill="#00B5E2"/>'
     '<rect y="66.6" width="200" height="33.4" rx="4" fill="#509E2F"/><rect y="66.6" width="200" height="13.4" fill="#509E2F"/>'
     '<circle cx="96" cy="50" r="15" fill="#FFFFFF"/><circle cx="100" cy="50" r="12.5" fill="#EF3340"/>'
     f'<polygon points="{star_points(110.5, 50, 8, 6.4, 3.1, rot=-90)}" fill="#FFFFFF"/></g>',
     ['national', 'zefer-gunu', 'musteqillik', 'bayraq-gunu'])

# nar: pomegranate (Azerbaijani symbol)
save('nar',
     '<path d="M84 44 L90 30 L96 40 L100 26 L104 40 L110 30 L116 44Z" fill="#9C1D2B"/>'
     '<circle cx="100" cy="110" r="66" fill="#C1272D"/>'
     '<path d="M58 86 C62 70 76 58 92 56" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" fill="none" opacity=".35"/>'
     '<path d="M100 48 C110 58 112 60 120 58" stroke="#9C1D2B" stroke-width="4" fill="none"/>',
     ['national', 'novruz', 'autumn', 'culture'])

# şəkərbura: half-moon pastry, pinched (naxış) rim, herringbone top (Novruz)
rim = ''.join(f'<circle cx="{100 + 84 * math.cos(math.radians(a)):.1f}" cy="{138 - 84 * math.sin(math.radians(a)) * .78:.1f}" r="7" fill="#D99A48"/>'
              for a in range(0, 181, 12))
herring = ''.join(f'<path d="M{100 + r * math.cos(math.radians(a)):.1f} {138 - r * math.sin(math.radians(a)) * .78:.1f} l{d * 7} -9" '
                  f'stroke="#B8732E" stroke-width="3.2" stroke-linecap="round"/>'
                  for r in (36, 54) for a in range(20, 161, 14) for d in (-1, 1))
save('sekerbura',
     rim + '<path d="M16 138 A84 65.5 0 0 1 184 138Z" fill="#EBC07F"/>'
     '<path d="M16 138 H184 C176 150 150 156 100 156 C50 156 24 150 16 138Z" fill="#D69A4A"/>'
     '<path d="M100 74 V134" stroke="#C98A3E" stroke-width="3" stroke-linecap="round"/>' + herring,
     ['novruz', 'food'])

# lalə: tulip (8 Mart, Ana günü, spring)
save('lale',
     '<path d="M100 110 V186" stroke="#3C7A3A" stroke-width="6" stroke-linecap="round"/>'
     '<path d="M100 170 C76 160 64 140 62 118 C80 126 94 142 100 162Z" fill="#4B8C45"/>'
     '<path d="M100 160 C122 150 134 132 138 110 C120 118 106 134 100 152Z" fill="#5BA052"/>'
     '<path d="M66 54 C64 90 76 116 100 118 C124 116 136 90 134 54 C122 66 112 70 100 52 C88 70 78 66 66 54Z" fill="#E63973"/>'
     '<path d="M100 52 C92 76 92 100 100 118 C108 100 108 76 100 52Z" fill="#F45D8F"/>',
     ['8-mart', 'ana-gunu', 'spring'])

# kublar: ABC blocks (children's day, child development)
def cube(x, y, s, top, left, right, ch):
    return (f'<path d="M{x} {y} l{s * .5} {-s * .28} l{s * .5} {s * .28} l{-s * .5} {s * .28}Z" fill="{top}"/>'
            f'<path d="M{x} {y} l{s * .5} {s * .28} v{s * .62} l{-s * .5} {-s * .28}Z" fill="{left}"/>'
            f'<path d="M{x + s * .5} {y + s * .28} l{s * .5} {-s * .28} v{s * .62} l{-s * .5} {s * .28}Z" fill="{right}"/>'
            f'<text x="{x + s * .25}" y="{y + s * .62}" font-family="Montserrat,Inter,Arial,sans-serif" font-weight="900" font-size="{s * .34}" '
            f'fill="#FFFFFF" text-anchor="middle" transform="skewY(30)" transform-origin="{x + s * .25} {y + s * .5}">{ch}</text>')
save('kublar', cube(30, 128, 70, '#FFD166', '#F4A300', '#D98C00', 'A') + cube(100, 128, 70, '#8ED1FC', '#3A86FF', '#2667CC', 'B')
     + cube(65, 88, 70, '#FF8FA3', '#E63946', '#B82E39', 'C'),
     ['1-iyun', 'children', 'inkisaf', 'education'])

# günəş: sun (summer, children's day, optimism)
rays = ''.join(f'<rect x="96" y="14" width="8" height="26" rx="4" fill="#FFB703" transform="rotate({k * 30} 100 100)"/>' for k in range(12))
save('gunes', rays + '<circle cx="100" cy="100" r="46" fill="#FFC93C"/><circle cx="100" cy="100" r="34" fill="#FFD95A"/>',
     ['1-iyun', 'summer', 'children', 'celebration'])

# konfetti: celebration scatter
bits = []
cols = ['#E63946', '#FFC93C', '#3A86FF', '#4CAF50', '#F45D8F', '#8E44AD']
for k in range(34):
    x, y = rng.uniform(10, 190), rng.uniform(10, 190)
    c = rng.choice(cols)
    if k % 3 == 0:
        bits.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(3, 6):.1f}" fill="{c}"/>')
    else:
        bits.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{rng.uniform(5, 9):.1f}" height="{rng.uniform(12, 18):.1f}" rx="2" fill="{c}" '
                    f'transform="rotate({rng.uniform(0, 180):.0f} {x:.1f} {y:.1f})"/>')
save('konfetti', ''.join(bits), ['celebration', 'birthday', 'yeni-il', 'launch'])

# hilal: crescent + star (Ramazan / Qurban bayramı)
save('hilal',
     '<circle cx="92" cy="100" r="64" fill="#E8B23A"/><circle cx="116" cy="88" r="56" fill="var(--bg, #FFFFFF)"/>'
     f'<polygon points="{star_points(140, 120, 5, 18, 8)}" fill="#E8B23A"/>',
     ['ramazan', 'qurban', 'religious'], tone='religious')

json.dump(MOTIFS, open(os.path.join(OUT, 'motifs.json'), 'w'), indent=2, ensure_ascii=False)
print(f'{len(MOTIFS)} motifs -> {os.path.relpath(OUT)}')
