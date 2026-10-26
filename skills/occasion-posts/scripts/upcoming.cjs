#!/usr/bin/env node
// List the occasions coming up, and scaffold a ready-to-render spec for one.
//
//   node upcoming.cjs [--days 45] [--from YYYY-MM-DD] [--niche speech,child-development] [--group az-national]
//   node upcoming.cjs --spec <id> [--format post|carousel] [--brand brands/x.json] [--out file.json]
//   node upcoming.cjs --show <id>
//
// Movable days (Novruz, çərşənbələr, Ramazan, Qurban, Mother's Day...) have no fixed date here;
// they are listed in their approximate month with "verify", never with an invented date.
'use strict';
const fs = require('fs');
const path = require('path');

const CAL = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'assets', 'calendar.json'), 'utf8'));
const LEAD = { remembrance: 3, religious: 5, awareness: 7, celebration: 7 };

const args = {};
for (let i = 2; i < process.argv.length; i++) {
  const t = process.argv[i];
  if (t.startsWith('--')) args[t.slice(2)] = process.argv[i + 1] && !process.argv[i + 1].startsWith('--') ? process.argv[++i] : true;
}
const die = m => { console.error(`✗ ${m}`); process.exit(2); };
const byId = id => CAL.occasions.find(o => o.id === id) || die(`Unknown occasion "${id}". Run without --spec to list ids.`);

if (args.show) {
  console.log(JSON.stringify({ ...byId(args.show), palette: CAL.palettes[byId(args.show).palette] }, null, 2));
  process.exit(0);
}

if (args.spec) {
  const o = byId(args.spec);
  const post = (args.format || 'post') === 'post';
  const motif = o.motifs[0];
  const date = o.date ? (() => { const [m, d] = o.date.split('-').map(Number);
    return `${d} ${['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avqust', 'sentyabr', 'oktyabr', 'noyabr', 'dekabr'][m - 1]}`; })() : '';
  const spec = {
    title: o.name.az,
    brand: args.brand || 'brands/my-brand.json',
    theme: 'minimal',
    tone: o.tone,
    format: post ? 'post' : 'carousel',
    ...(o.palette && o.tone !== 'remembrance' ? { palette: CAL.palettes[o.palette] } : {}),
    ...(!post && o.tone === 'celebration' && o.motifs.includes('konfetti') ? { ornament: 'konfetti' } : {}),
    slides: post
      ? [{ type: 'greeting', motif, kicker: date, title: o.name.az, message: 'MESAJ: 1-2 cümlə, səmimi, auditoriyaya birbaşa.' }]
      : [
          { type: 'cover', motif, kicker: date || o.name.az, title: 'BAŞLIQ: 6 sözə qədər', subtitle: o.angles[0] },
          { type: 'text', title: 'NİYƏ BU GÜN: qısa kontekst', body: 'Faktı yalnız etibarlı mənbədən yaz.' },
          { type: 'list', title: 'PRAKTİK HİSSƏ', items: ['...', '...', '...'] },
          o.tone === 'remembrance'
            ? { type: 'greeting', motif: 'qerenfil', title: 'Anma cümləsi', message: '...' }
            : { type: 'cta', title: 'YEKUN: bir aydın addım', action: 'Paylaş', icon: 'share' },
        ],
    _occasion: { id: o.id, avoid: o.avoid || [], angles: o.angles, ai_prompt: o.ai_prompt || null, verify: !!o.verify, note: o.note || null },
  };
  const out = args.out || `${o.id}.json`;
  fs.writeFileSync(out, JSON.stringify(spec, null, 2) + '\n');
  console.log(`wrote ${out}  (tone: ${o.tone}${o.verify ? ', DATE MUST BE VERIFIED' : ''})`);
  if (o.avoid) console.log(`avoid: ${o.avoid.join(' · ')}`);
  process.exit(0);
}

const from = args.from ? new Date(args.from + 'T00:00:00') : new Date(new Date().toDateString());
if (isNaN(from)) die('--from must be YYYY-MM-DD');
const days = +(args.days || 45);
const niches = args.niche ? String(args.niche).split(',') : null;
const group = args.group || null;
const keep = o => (!niches || (o.niches || []).some(n => niches.includes(n)) || (!o.niches && (o.groups || []).includes('az-national')))
  && (!group || o.groups.includes(group));

const rows = [];
for (const o of CAL.occasions.filter(keep)) {
  if (o.date) {
    const [m, d] = o.date.split('-').map(Number);
    for (const y of [from.getFullYear(), from.getFullYear() + 1]) {
      const at = new Date(y, m - 1, d);
      const diff = Math.round((at - from) / 864e5);
      if (diff >= 0 && diff <= days) { rows.push({ at, diff, o }); break; }
    }
  } else {
    const months = String(o.approx_month || '').match(/\d+/g) || [];
    const end = new Date(from.getTime() + days * 864e5);
    const inWindow = months.some(mm => { for (let t = new Date(from); t <= end; t.setDate(t.getDate() + 1)) if (t.getMonth() + 1 === +mm) return true; return false; });
    if (inWindow || o.approx_month === 'hicri təqvim') rows.push({ at: null, diff: null, o });
  }
}
rows.sort((a, b) => (a.diff == null) - (b.diff == null) || a.diff - b.diff);
const fmt = d => d.toISOString().slice(0, 10);
console.log(`Occasions ${fmt(from)} → +${days} days${niches ? ` · niche: ${niches.join(',')}` : ''}\n`);
for (const { at, diff, o } of rows) {
  const lead = LEAD[o.tone] || 7;
  const when = at ? `${fmt(at)} (${diff === 0 ? 'today' : `in ${diff}d`}, prepare by ${fmt(new Date(at.getTime() - lead * 864e5))})` : `date varies: ${o.rule || o.approx_month} VERIFY`;
  console.log(`${o.tone.padEnd(12)} ${o.name.az}\n             ${when}\n             id: ${o.id} · motifs: ${o.motifs.join(', ')}${o.note ? `\n             note: ${o.note}` : ''}\n`);
}
if (!rows.length) console.log('Nothing in this window. Widen --days or drop --niche.');
