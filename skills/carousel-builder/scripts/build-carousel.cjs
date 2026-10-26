#!/usr/bin/env node
// Render a carousel spec (JSON) into upload-ready slides: PNGs, a PDF, a contact sheet and a
// QA report. One command, no design tool. See ../SKILL.md for the workflow and the spec format.
//
//   node build-carousel.cjs <spec.json> [--brand kit.json] [--theme name|all] [--size WxH|portrait|square]
//                                      [--out dir] [--no-pdf] [--jpeg]
//   node build-carousel.cjs --init <dir>     copy an example spec + brand kit to start from
//   node build-carousel.cjs --themes         list the themes
//
// Exit code: 0 = shipped (warnings allowed), 1 = QA errors to fix, 2 = bad input / setup.
'use strict';

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const THEMES_DIR = path.join(SKILL_DIR, 'assets', 'themes');
const EXAMPLES_DIR = path.join(SKILL_DIR, 'assets', 'examples');
const MOTIFS_DIR = path.join(SKILL_DIR, 'assets', 'motifs');
const MOTIFS = JSON.parse(fs.readFileSync(path.join(MOTIFS_DIR, 'motifs.json'), 'utf8'));
const THEMES = JSON.parse(fs.readFileSync(path.join(THEMES_DIR, 'themes.json'), 'utf8'));

const SIZES = { portrait: [1080, 1350], square: [1080, 1080], linkedin: [1080, 1350], story: [1080, 1920] };
// Instagram draws its own UI over the top and bottom of a Story; text must stay out of it.
const STORY_SAFE = { top: 250, bottom: 340 };
const STRINGS = {
  az: { swipe: 'Sürüşdür', save: 'Yadda saxla', source: 'Mənbə', answer: 'Düzgün cavab', quizHint: 'Cavab son slaydda' },
  en: { swipe: 'Swipe', save: 'Save this', source: 'Source', answer: 'Answer', quizHint: 'Answer on the last slide' },
  ru: { swipe: 'Листай', save: 'Сохрани', source: 'Источник', answer: 'Правильный ответ', quizHint: 'Ответ на последнем слайде' },
  tr: { swipe: 'Kaydır', save: 'Kaydet', source: 'Kaynak', answer: 'Doğru cevap', quizHint: 'Cevap son slaytta' },
};
// Line icons (24px grid, stroke = currentColor) so arrows and checks are crisp in every font.
const ICON_PATHS = {
  arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  x: '<path d="M6 6l12 12M18 6L6 18"/>',
  save: '<path d="M6 3.5h12v17l-6-4.5-6 4.5z"/>',
  share: '<path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/>',
  comment: '<path d="M20 11.5a8 8 0 0 1-11.6 7.1L4 20l1.4-4.2A8 8 0 1 1 20 11.5z"/>',
  follow: '<path d="M15 19a6 6 0 0 0-12 0M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM19 8v6M16 11h6"/>',
  link: '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3.2-3.2a4.5 4.5 0 0 0-6.4-6.4l-1 1M14 10a4.5 4.5 0 0 0-6.4 0l-3.2 3.2a4.5 4.5 0 0 0 6.4 6.4l1-1"/>',
};
const icon = (name, cls = '') => `<svg class="ic ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON_PATHS[name]}</svg>`;
const SLIDE_TYPES = ['cover', 'text', 'list', 'stat', 'quote', 'compare', 'image', 'recap', 'cta',
  'greeting', 'poster', 'meme', 'comic', 'quiz', 'answer', 'table', 'annotated'];
const REQUIRED = { cover: ['title'], text: ['title'], list: ['items'], stat: ['value', 'label'], quote: ['quote'],
  compare: ['left', 'right'], image: ['src'], recap: ['items'], cta: ['title'], greeting: ['title'], poster: ['title'],
  meme: ['caption'], comic: ['panels'], quiz: ['question', 'options'], answer: ['options', 'correct'], table: ['rows'],
  annotated: ['image', 'notes'] };
// Tone sets what a post may do. Remembrance days (20 Yanvar, 26 Fevral, 31 Mart, 27 Sentyabr) get a
// fixed sober palette and no selling, jokes or "save this" asks; the QA enforces it.
const TONES = ['celebration', 'awareness', 'remembrance', 'religious', 'neutral'];
const REMEMBRANCE_PALETTE = { bg: '#121315', surface: '#1C1D20', text: '#F2F0EB', muted: '#A9A6A0', accent: '#B3122E', accentInk: '#FFFFFF' };
const NOT_IN = {
  remembrance: { types: ['poster', 'meme', 'comic', 'quiz', 'answer', 'stat'], motifs: ['sam', 'qerenfil', 'bayraq'], icons: ['save', 'link', 'follow'] },
  religious: { types: ['meme', 'comic'], motifs: null, icons: [] },
};
const DEFAULT_BRAND = {
  name: 'Brand',
  handle: '@brand',
  language: 'az',
  logo: null,
  colors: { bg: '#F7F5F0', surface: '#FFFFFF', text: '#14161A', muted: '#5B616B', accent: '#E8462E' },
  fonts: {},
};

// ---------- CLI ----------

function die(msg, code = 2) { console.error(`✗ ${msg}`); process.exit(code); }

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--no-pdf') a.noPdf = true;
    else if (t === '--jpeg') a.jpeg = true;
    else if (t === '--themes') a.listThemes = true;
    else if (t.startsWith('--')) a[t.slice(2)] = argv[++i];
    else a._.push(t);
  }
  return a;
}

function readJson(p, what) {
  if (!fs.existsSync(p)) die(`${what} not found: ${p}`);
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { die(`${what} is not valid JSON (${p}): ${e.message}`); }
}

// ---------- colour helpers ----------

function hexToRgb(hex) {
  const m = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(String(hex).trim());
  if (!m) return null;
  let h = m[1];
  if (h.length === 3) h = h.split('').map(c => c + c).join('');
  return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16));
}
function luminance([r, g, b]) {
  const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function contrast(a, b) {
  const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
}
function inkFor(hex) {
  const rgb = hexToRgb(hex);
  return contrast(rgb, [255, 255, 255]) >= contrast(rgb, [17, 17, 17]) ? '#FFFFFF' : '#111111';
}

// ---------- brand + spec ----------

function loadBrand(spec, specDir, cliBrand) {
  let raw = {}, brandDir = specDir;
  const ref = cliBrand || spec.brand;
  if (typeof ref === 'string') {
    const p = path.resolve(cliBrand ? process.cwd() : specDir, ref);
    raw = readJson(p, 'Brand kit');
    brandDir = path.dirname(p);
  } else if (ref && typeof ref === 'object') raw = ref;

  const b = {
    ...DEFAULT_BRAND, ...raw,
    colors: { ...DEFAULT_BRAND.colors, ...(raw.colors || {}) },
    fonts: { ...(raw.fonts || {}) },
  };
  for (const [k, v] of Object.entries(b.colors)) {
    if (!hexToRgb(v)) die(`Brand colour "${k}" must be a hex value like #1A2B3C, got "${v}"`);
  }
  b.colors.accentInk = b.colors.accentInk || inkFor(b.colors.accent);
  if (b.handle && !b.handle.startsWith('@')) b.handle = '@' + b.handle;
  if (b.logo) {
    const lp = path.resolve(brandDir, b.logo);
    if (!fs.existsSync(lp)) die(`Brand logo not found: ${lp}`);
    b.logoUrl = 'file://' + lp;
  }
  b.fontFiles = (raw.fonts && raw.fonts.files || []).map(f => {
    const fp = path.resolve(brandDir, f.src);
    if (!fs.existsSync(fp)) die(`Brand font file not found: ${fp}`);
    return { ...f, url: 'file://' + fp };
  });
  return b;
}

function resolveSize(v) {
  if (!v) return SIZES.portrait;
  if (SIZES[v]) return SIZES[v];
  const m = /^(\d{3,4})x(\d{3,4})$/.exec(v);
  if (!m) die(`Size must be portrait, square, story, linkedin or WxH (e.g. 1080x1350), got "${v}"`);
  return [+m[1], +m[2]];
}

function validateSlides(spec, specDir) {
  if (!Array.isArray(spec.slides) || !spec.slides.length) die('Spec needs a non-empty "slides" array');
  spec.slides.forEach((s, i) => {
    const where = `slide ${i + 1}`;
    if (!SLIDE_TYPES.includes(s.type)) die(`${where}: unknown type "${s.type}". Use one of: ${SLIDE_TYPES.join(', ')}`);
    for (const k of REQUIRED[s.type]) if (s[k] == null || s[k] === '') die(`${where} (${s.type}) is missing "${k}"`);
    const file = (rel, what) => {
      const p = path.resolve(specDir, rel);
      if (!fs.existsSync(p)) die(`${where}: ${what} not found: ${p}`);
      return 'file://' + p;
    };
    const img = s.type === 'image' ? s.src : s.image;
    if (img) s._src = file(img, 'image');
    const motif = m => { if (m && !MOTIFS[m]) die(`${where}: unknown motif "${m}". Motifs: ${Object.keys(MOTIFS).join(', ')}`); };
    motif(s.motif);
    if (s.type === 'comic') {
      if (!Array.isArray(s.panels) || s.panels.length < 2 || s.panels.length > 4) die(`${where}: comic needs 2-4 panels`);
      s.panels.forEach(pn => { motif(pn.motif); if (pn.image) pn._src = file(pn.image, 'panel image'); });
    }
    if (s.type === 'annotated') {
      if (!Array.isArray(s.notes) || !s.notes.length || s.notes.length > 5) die(`${where}: annotated needs 1-5 notes`);
      s.notes.forEach((nt, k) => { if (!(nt.x >= 0 && nt.x <= 100 && nt.y >= 0 && nt.y <= 100 && nt.text)) die(`${where}: note ${k + 1} needs x and y (0-100, % of the image) and text`); });
    }
    if ((s.type === 'quiz' || s.type === 'answer') && (!Array.isArray(s.options) || s.options.length < 2 || s.options.length > 4)) die(`${where}: ${s.type} needs 2-4 options`);
    if (s.type === 'answer') {
      const c = typeof s.correct === 'string' ? 'ABCD'.indexOf(s.correct.toUpperCase()) : s.correct;
      if (!(c >= 0 && c < s.options.length)) die(`${where}: "correct" must be a letter (A-D) or index of an option`);
      s._correct = c;
    }
    if (s.icon && !ICON_PATHS[s.icon]) die(`${where}: unknown icon "${s.icon}". Use one of: save, share, comment, follow, link`);
  });
  if (spec.ornament && !MOTIFS[spec.ornament]) die(`Unknown ornament motif "${spec.ornament}". Motifs: ${Object.keys(MOTIFS).join(', ')}`);
  if (spec.tone && !TONES.includes(spec.tone)) die(`Unknown tone "${spec.tone}". Use one of: ${TONES.join(', ')}`);
  if (spec.format && !['carousel', 'post'].includes(spec.format)) die('format must be "carousel" or "post"');
}

// ---------- spec-level QA (copy discipline) ----------

const words = t => String(t || '').replace(/\*\*/g, '').split(/\s+/).filter(Boolean).length;

function copyChecks(spec) {
  const slides = spec.slides, out = [];
  const add = (i, level, code, msg) => out.push({ slide: i + 1, level, code, msg });
  const n = slides.length;
  const tone = spec.tone || 'neutral';
  const rule = NOT_IN[tone];
  if (rule) {
    slides.forEach((s, i) => {
      if (rule.types.includes(s.type)) add(i, 'error', 'tone-type', `A "${s.type}" slide does not belong in a ${tone} post. Keep it to remembrance, information and respect.`);
      const ms = [s.motif, ...(s.panels || []).map(p => p.motif), i === 0 ? spec.ornament : null].filter(Boolean);
      if (rule.motifs) for (const m of ms) if (!rule.motifs.includes(m)) add(i, 'error', 'tone-motif', `Motif "${m}" is wrong for a ${tone} post. Use: ${rule.motifs.join(', ')}.`);
      if (s.type === 'cta' && rule.icons.includes(s.icon || 'save')) add(i, 'error', 'tone-cta', `A "${s.icon || 'save'}" ask is wrong on a ${tone} day. Close with a line of remembrance, or no CTA.`);
      if (s.accent) add(i, 'warn', 'tone-accent', 'Accent-colour slides read as celebration. Drop "accent" on this day.');
    });
  }
  if (spec.format === 'post') {
    slides.forEach((s, i) => {
      if (words(s.title) > 10) add(i, 'warn', 'title-wordy', `Headline is ${words(s.title)} words. A single post must land in one glance.`);
    });
    return out;
  }
  if (n > 20) add(-1, 'error', 'too-many-slides', `${n} slides. Instagram's cap is 20 (verify-quarterly), and 6-10 is where strong carousels live.`);
  else if (n > 12) add(-1, 'warn', 'long-carousel', `${n} slides. Most strong carousels are 6-10; cut the weakest.`);
  else if (n < 4) add(-1, 'warn', 'short-carousel', `${n} slides. Under 4 the swipe rarely starts; is this a single image?`);
  if (slides[0].type !== 'cover') add(0, 'warn', 'no-cover', 'Slide 1 is not a cover. The cover decides whether anyone swipes.');
  if (slides[n - 1].type !== 'cta') add(n - 1, 'info', 'no-cta', 'Last slide is not a CTA. One ask (usually save) is the default ending.');
  slides.forEach((s, i) => {
    if (s.type === 'cover' && words(s.title) > 8) add(i, 'warn', 'cover-wordy', `Cover title is ${words(s.title)} words. Aim for 6 or fewer; it must read at thumbnail size.`);
    if (s.title && s.type !== 'cover' && words(s.title) > 10) add(i, 'warn', 'title-wordy', `Title is ${words(s.title)} words. Keep slide headlines to 3-7.`);
    const body = [s.body, s.subtitle, s.caption, s.message, s.explanation, ...(s.notes || []).map(nt => nt.text), ...(s.items || []), ...(s.options || []),
      ...(s.details || []).map(d => typeof d === 'string' ? d : `${d.label} ${d.value}`)].map(words).reduce((a, b) => a + b, 0);
    const limit = s.type === 'recap' || s.type === 'answer' ? 45 : s.type === 'table' ? 999 : 30;
    if (body > limit) add(i, 'warn', 'wall-of-text', `${body} words under the headline. Over ${limit} reads as a paragraph; split into two slides.`);
    if (s.type === 'stat' && !s.source) add(i, 'warn', 'unsourced-stat', 'Stat has no "source". Never ship a number you cannot point to.');
    if (s.type === 'table' && s.rows.length > 7) add(i, 'warn', 'long-table', `${s.rows.length} rows. Over 7 gets too small to read; split the table.`);
    if (s.type === 'answer' && !slides.slice(0, i).some(x => x.type === 'quiz')) add(i, 'warn', 'answer-without-quiz', 'Answer slide with no quiz slide before it.');
    if ((s.type === 'list' || s.type === 'recap') && s.items.length > 6) add(i, 'warn', 'long-list', `${s.items.length} items on one slide. Keep to 6 or fewer.`);
  });
  return out;
}

// ---------- HTML ----------

const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// **highlight** -> accent; newline -> line break; hyphenated words (bio-nun, Highlight-lar) never
// split at the hyphen. Everything else is escaped text.
const rich = s => esc(s)
  .replace(/[^\s*]+-[^\s*]+/g, w => `<span class="nw">${w}</span>`)
  .replace(/\*\*(.+?)\*\*/g, '<strong class="hl">$1</strong>').replace(/\n/g, '<br>');
const pad2 = n => String(n).padStart(2, '0');

function initials(name) {
  return String(name).split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0]).join('').toUpperCase();
}

const motifCache = new Map();
function motifSvg(name) {
  if (!motifCache.has(name)) motifCache.set(name, fs.readFileSync(path.join(MOTIFS_DIR, `${name}.svg`), 'utf8').trim());
  return motifCache.get(name);
}
// A slide's picture: the user's photo wins, then a library motif, else nothing.
const visual = x => x._src ? `<img src="${esc(x._src)}" alt="${esc(x.alt || '')}">` : x.motif ? motifSvg(x.motif) : '';

function slideInner(s, ctx) {
  const L = ctx.L;
  const T = (cls, txt, fit = true, tag = 'div') => txt ? `<${tag} class="${cls} tx"${fit ? ' data-fit' : ''}>${rich(txt)}</${tag}>` : '';
  const num = s.number != null ? `<div class="num tx">${esc(s.number)}</div>` : '';
  switch (s.type) {
    case 'cover':
      return `${s.motif && !s._src ? `<div class="cover-art">${motifSvg(s.motif)}</div>` : ''}${s.kicker ? `<div class="kicker-wrap">${T('kicker', s.kicker, false)}</div>` : ''}${T('title', s.title, true, 'h1')}${T('sub', s.subtitle)}`;
    case 'text':
      // "reserve": an empty band where a real Instagram sticker (poll, question, link) is added by hand
      // in the app. Nothing is drawn there: a picture of a sticker is not a sticker.
      return `${num}<div class="bar"></div>${T('h2', s.title, true, 'h2')}${T('body', s.body, true, 'p')}` +
        (s.reserve ? `<div class="reserve" data-sticker="${esc(s.reserve)}"></div>` : '');
    case 'list': {
      const tag = s.numbered === false ? 'ul' : 'ol';
      const items = s.items.map((it, k) => `<li><span class="marker tx">${tag === 'ol' ? pad2(k + 1) : '•'}</span><span class="li-text tx" data-fit>${rich(it)}</span></li>`).join('');
      return `${num}<div class="bar"></div>${T('h2', s.title, true, 'h2')}<${tag} class="list">${items}</${tag}>`;
    }
    case 'stat':
      return `${T('kicker', s.kicker, false)}${T('stat-value', s.value)}${T('stat-label', s.label)}` +
        (s.source ? `<div class="source tx">${esc(L.source)}: ${esc(s.source)}</div>` : '');
    case 'quote':
      return `<div class="qmark">“</div>${T('quote', s.quote, true, 'blockquote')}` +
        (s.author ? `<div class="author tx">— ${esc(s.author)}</div>` : '');
    case 'compare': {
      const col = (c, kind) => `<div class="col col-${kind}"><div class="col-head">${icon(kind === 'bad' ? 'x' : 'check', 'col-ic')}` +
        `${c.label ? `<span class="col-label tx">${esc(c.label)}</span>` : ''}</div>` +
        `<ul>${(c.items || []).map(it => `<li class="tx" data-fit>${rich(it)}</li>`).join('')}</ul></div>`;
      return `${T('h2', s.title, true, 'h2')}<div class="compare">${col(s.left, 'bad')}${col(s.right, 'good')}</div>`;
    }
    case 'image':
      return `<div class="img-wrap"><img src="${esc(s._src)}" alt="${esc(s.alt || s.title || '')}"></div>` +
        `<div class="img-text">${T('h2', s.title, true, 'h2')}${T('body', s.caption, true, 'p')}</div>`;
    case 'recap': {
      const items = s.items.map(it => `<li><span class="check">${icon('check')}</span><span class="li-text tx" data-fit>${rich(it)}</span></li>`).join('');
      return `${T('kicker', s.kicker, false)}${T('h2', s.title, true, 'h2')}<ul class="checks">${items}</ul>`;
    }
    case 'cta':
      return `<div class="cta-card"><div class="avatar avatar-lg">${ctx.avatar}</div>` +
        `<div><div class="cta-name tx">${esc(ctx.brand.name)}</div><div class="cta-handle tx">${esc(ctx.brand.handle)}</div></div></div>` +
        `${T('h2', s.title, true, 'h2')}${T('body', s.body, true, 'p')}` +
        `<div class="action">${icon(s.icon || 'save')}<span class="tx">${esc(s.action || L.save)}</span></div>`;
    case 'greeting':
      return `${visual(s) ? `<div class="g-art">${visual(s)}</div>` : ''}` +
        `${s.kicker ? `<div class="kicker-wrap">${T('kicker', s.kicker, false)}</div>` : ''}` +
        `${T('h2 g-title', s.title, true, 'h2')}${T('body g-msg', s.message || s.body, true, 'p')}` +
        `<div class="g-sign tx">${esc(s.signature || ctx.brand.name)}</div>`;
    case 'poster': {
      const details = (s.details || []).map(d => typeof d === 'string'
        ? `<li class="tx" data-fit>${rich(d)}</li>`
        : `<li><span class="d-label tx">${esc(d.label)}</span><span class="d-value tx" data-fit>${rich(d.value)}</span></li>`).join('');
      return `${visual(s) ? `<div class="p-art">${visual(s)}</div>` : ''}<div class="p-body">` +
        `${s.badge ? `<div class="p-badge tx">${esc(s.badge)}</div>` : ''}` +
        `${s.kicker ? `<div class="kicker-wrap">${T('kicker', s.kicker, false)}</div>` : ''}` +
        `${T('h2 p-title', s.title, true, 'h2')}${T('body', s.body, true, 'p')}` +
        `${details ? `<ul class="p-details">${details}</ul>` : ''}` +
        `${s.action ? `<div class="action">${icon(s.icon || 'arrow')}<span class="tx">${esc(s.action)}</span></div>` : ''}` +
        `${s.contact ? `<div class="p-contact tx">${esc(s.contact)}</div>` : ''}</div>`;
    }
    case 'meme':
      return `<div class="m-cap tx" data-fit>${rich(s.caption)}</div>` +
        `<div class="m-art${s._src ? ' is-photo' : ''}">${visual(s)}${s.bottom ? `<div class="m-bottom tx" data-fit>${rich(s.bottom)}</div>` : ''}</div>` +
        `${s.credit ? `<div class="source tx">${esc(s.credit)}</div>` : ''}`;
    case 'comic':
      return `${T('h2 c-title', s.title, true, 'h2')}<div class="comic n${s.panels.length}">` +
        s.panels.map((pn, k) => `<div class="panel"><div class="pn-no">${k + 1}</div><div class="pn-art${pn._src ? ' is-photo' : ''}">${visual(pn)}</div>` +
          `${pn.text ? `<div class="pn-text tx" data-fit>${rich(pn.text)}</div>` : ''}</div>`).join('') + '</div>';
    case 'quiz':
    case 'answer': {
      const isA = s.type === 'answer';
      const opts = s.options.map((o, k) => `<li class="${isA ? (k === s._correct ? 'right' : 'wrong') : ''}">` +
        `<span class="opt-l">${isA && k === s._correct ? icon('check') : 'ABCD'[k]}</span><span class="opt-t tx" data-fit>${rich(o)}</span></li>`).join('');
      return `<div class="kicker-wrap">${T('kicker', s.kicker || (isA ? L.answer : 'Test'), false)}</div>` +
        `${T('h2 q-title', s.question, true, 'h2')}<ol class="opts">${opts}</ol>` +
        (isA ? T('body q-expl', s.explanation, true, 'p') : `<div class="source tx">${esc(s.hint != null ? s.hint : L.quizHint)}</div>`);
    }
    case 'annotated': {
      // Numbered pins on the picture, the same numbers in a legend below it.
      const pins = s.notes.map((nt, k) => `<span class="pin" style="left:${nt.x}%;top:${nt.y}%">${k + 1}</span>`).join('');
      const legend = s.notes.map((nt, k) => `<li><span class="pin-no">${k + 1}</span><span class="tx" data-fit>${rich(nt.text)}</span></li>`).join('');
      return `${T('h2 an-title', s.title, true, 'h2')}<div class="an-art"><div class="an-box"><img src="${esc(s._src)}" alt="${esc(s.alt || s.title || '')}">${pins}</div></div>` +
        `<ol class="an-notes">${legend}</ol>`;
    }
    case 'table': {
      const head = (s.columns || []).map(c => `<th class="tx">${esc(c)}</th>`).join('');
      const rows = s.rows.map(r => `<tr>${r.map((c, k) => `<td class="tx${k === 0 ? ' td-key' : ''}" data-fit>${rich(c)}</td>`).join('')}</tr>`).join('');
      return `${T('h2 t-title', s.title, true, 'h2')}<table class="tbl">${head ? `<thead><tr>${head}</tr></thead>` : ''}<tbody>${rows}</tbody></table>` +
        (s.note ? `<div class="source tx">${esc(s.note)}</div>` : '');
    }
  }
}

// One continuous line drawn across all slides; each slide shows its own window of it, so the
// carousel reads as one piece when swiped. Deterministic: same slide count, same line.
function panorama(W, H, n) {
  const total = n * W, y0 = H - 108, amp = 34;
  let d = `M ${-40} ${y0}`;
  const dots = [];
  for (let k = 0; k < n * 2; k++) {
    const x1 = k * W / 2, x2 = x1 + W / 2, dir = k % 2 ? 1 : -1;
    d += ` C ${x1 + W / 6} ${y0 + dir * amp}, ${x2 - W / 6} ${y0 + dir * amp}, ${x2} ${y0}`;
    if (k % 2) dots.push(`<circle class="pano-dot" cx="${x2}" cy="${y0}" r="9"/>`);
  }
  return `<path class="pano-line" d="${d} L ${total + 40} ${y0}" fill="none"/>${dots.join('')}`;
}

function buildHtml({ spec, brand, theme, themeCss, baseCss, fontCss, W, H }) {
  const L = STRINGS[brand.language] || STRINGS.en;
  const tdef = THEMES[theme];
  const f = { heading: brand.fonts.heading || tdef.fonts.heading, body: brand.fonts.body || tdef.fonts.body,
    display: brand.fonts.display || tdef.fonts.display || brand.fonts.heading || tdef.fonts.heading,
    mono: brand.fonts.mono || tdef.fonts.mono };
  const stack = (fam, fb) => `"${fam}", ${fb}`;
  const c = brand.colors;
  const n = spec.slides.length;
  let auto = 0;
  const autoNumber = spec.autoNumber != null ? spec.autoNumber : !!tdef.autoNumber;

  const logo = brand.logoUrl ? `<img class="logo" src="${esc(brand.logoUrl)}" alt="">` : '';
  const avatar = brand.logoUrl ? `<img src="${esc(brand.logoUrl)}" alt="">` : `<span>${esc(initials(brand.name))}</span>`;

  // "byline": "line" in the brand kit swaps the avatar badge for a signature line: NAME ——— RUBRIC
  const byline = brand.byline === 'line'
    ? `<div class="byline"><span class="by-name tx">${esc(brand.name)}</span><span class="by-rule"></span>${spec.rubric ? `<span class="by-rub tx">${esc(spec.rubric)}</span>` : ''}</div>`
    : '';

  const pano = panorama(W, H, n);
  const isPost = spec.format === 'post';
  const orn = spec.ornament ? `<div class="orn orn-a">${motifSvg(spec.ornament)}</div><div class="orn orn-b">${motifSvg(spec.ornament)}</div>` : '';
  const slides = spec.slides.map((s, i) => {
    if (autoNumber && (s.type === 'text' || s.type === 'list') && s.number == null) s.number = pad2(++auto);
    const isCover = s.type === 'cover', isLast = i === n - 1;
    const photo = isCover && s._src;
    const rail = Array.from({ length: n }, (_, k) => `<i class="${k < i ? 'done' : k === i ? 'on' : ''}"></i>`).join('');
    const swipe = isLast || isPost ? '' : `<div class="swipe">${isCover ? `<span class="swipe-label tx">${esc(L.swipe)}</span>` : ''}<span class="swipe-btn">${icon('arrow')}</span></div>`;
    const count = isCover || isPost ? '' : `<div class="count tx">${i + 1} / ${n}</div>`;
    return `<section class="slide t-${s.type}${s.accent ? ' is-accent' : ''}${photo ? ' has-photo' : ''}" data-index="${i + 1}" data-type="${s.type}">
  ${photo ? `<div class="cover-photo"><img src="${esc(s._src)}" alt=""></div><div class="shade"></div>` : ''}
  <div class="deco"><svg class="pano" viewBox="0 0 ${n * W} ${H}" width="${n * W}" height="${H}" style="left:${-i * W}px" aria-hidden="true">${pano}</svg>
    ${isCover || isLast || isPost ? '' : `<div class="ghost">${pad2(i + 1)}</div>`}${orn}<div class="grain"></div></div>
  <div class="frame"${photo ? ' data-qa-bg="#0B0C0E"' : ''}>
    <div class="rail">${rail}</div>
    <div class="top">${byline || `<div class="badge"><div class="avatar">${avatar}</div><div class="badge-text"><div class="pname tx">${esc(brand.name)}</div><div class="phandle tx">${esc(brand.handle)}</div></div></div>`}${count}</div>
    <div class="content">${slideInner(s, { L, brand, avatar })}</div>
    <footer class="foot"><div class="brandmark">${logo}<span class="handle tx">${esc(brand.handle)}</span></div>${swipe}</footer>
  </div>
</section>`;
  }).join('\n');

  const faces = brand.fontFiles.map(ff => `@font-face{font-family:"${ff.family}";src:url("${ff.url}");font-weight:${ff.weight || 400};font-style:${ff.style || 'normal'};font-display:block}`).join('\n');

  return `<!doctype html>
<html lang="${esc(brand.language)}"><head><meta charset="utf-8"><title>${esc(spec.title || 'carousel')}</title>
<style>${fontCss}
${faces}
:root{--W:${W}px;--H:${H}px;
--bg:${c.bg};--surface:${c.surface};--text:${c.text};--muted:${c.muted};--accent:${c.accent};--accent-ink:${c.accentInk};
--font-head:${stack(f.heading, '"Inter", "Helvetica Neue", Arial, sans-serif')};
--font-body:${stack(f.body, '"Inter", "Helvetica Neue", Arial, sans-serif')};
--font-display:${stack(f.display, 'Georgia, "Times New Roman", serif')};
--font-mono:${stack(f.mono || 'DejaVu Sans Mono', '"DejaVu Sans Mono", Menlo, monospace')};}
@page{size:${W}px ${H}px;margin:0}
</style>
<style>${baseCss}</style>
<style>${themeCss}</style>
</head><body class="theme-${theme} ${H / W >= 1.7 ? 'size-story ' : ''}tone-${esc(spec.tone || 'neutral')} format-${isPost ? 'post' : 'carousel'}">
${slides}
</body></html>`;
}

// ---------- fonts ----------

async function googleFontCss(browser, families) {
  const page = await browser.newPage();
  const css = [], missing = [];
  for (const fam of families) {
    const q = encodeURIComponent(fam).replace(/%20/g, '+');
    const tries = [`ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700`, `wght@400;500;600;700;800;900`, `wght@400;700`, ''];
    let ok = false;
    for (const axes of tries) {
      const url = `https://fonts.googleapis.com/css2?family=${q}${axes ? ':' + axes : ''}&display=block`;
      try {
        const r = await page.goto(url, { timeout: 15000 });
        if (r && r.status() === 200) { css.push(await r.text()); ok = true; break; }
      } catch (_) { break; } // offline: stop trying this family
    }
    if (!ok) missing.push(fam);
  }
  await page.close();
  return { css: css.join('\n'), missing };
}

// ---------- in-page fit + QA ----------
// Runs inside Chromium. Shrinks [data-fit] text until the slide's content fits, then checks
// overflow, safe zones, contrast, small type and glyph coverage (e.g. Azerbaijani ə, ğ, ı).
function pageQa(opts) {
  const issues = [];
  const add = (slide, level, code, msg) => issues.push({ slide, level, code, msg });
  // rgb()/rgba() report 0-255; color(srgb ...) (what color-mix() computes to) reports 0-1.
  const parse = c => {
    const m = c.match(/[\d.]+/g);
    if (!m) return [0, 0, 0, 0];
    const v = m.map(Number);
    if (c.startsWith('color(')) return [v[0] * 255, v[1] * 255, v[2] * 255, v.length > 3 ? v[3] : 1];
    return v;
  };
  const lum = ([r, g, b]) => [r, g, b].map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; })
    .reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const bgOf = el => {
    for (let e = el; e; e = e.parentElement) {
      if (e.dataset && e.dataset.qaBg) { const h = e.dataset.qaBg.slice(1); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); }
      const cs = getComputedStyle(e), c = parse(cs.backgroundColor);
      if (c.length === 4 ? c[3] > 0.5 : !/^rgba\(0, 0, 0, 0\)$|^transparent$/.test(cs.backgroundColor)) return c.slice(0, 3);
    }
    return [255, 255, 255];
  };
  const ctx = document.createElement('canvas').getContext('2d');
  const missingGlyph = new Map();
  const fontCache = new Map();

  document.querySelectorAll('.slide').forEach(slide => {
    const idx = +slide.dataset.index;
    const content = slide.querySelector('.content');
    const fits = [...slide.querySelectorAll('[data-fit]')];
    fits.forEach(el => { el.dataset.base = parseFloat(getComputedStyle(el).fontSize); });
    const over = () => content.scrollHeight > content.clientHeight + 1 || content.scrollWidth > content.clientWidth + 1;
    let scale = 1;
    while (over() && scale > opts.minScale) {
      scale = Math.round((scale - 0.03) * 100) / 100;
      fits.forEach(el => { el.style.fontSize = (el.dataset.base * scale) + 'px'; });
    }
    if (over()) add(idx, 'error', 'overflow', `Text does not fit even at ${Math.round(scale * 100)}% size. Cut words or split the slide.`);
    else if (scale < 1) add(idx, scale < 0.8 ? 'warn' : 'info', 'shrunk', `Text auto-shrunk to ${Math.round(scale * 100)}% to fit.${scale < 0.8 ? ' It is getting small; consider cutting words.' : ''}`);

    const S = slide.getBoundingClientRect();
    const isCover = slide.dataset.type === 'cover';
    slide.querySelectorAll('.tx').forEach(el => {
      if (!el.textContent.trim() || el.offsetParent === null) return;
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 600;
      const snippet = el.textContent.trim().slice(0, 40);
      const m = opts.safe, side = isCover ? opts.coverSide : m;
      if (opts.story && (r.top - S.top < opts.story.top - 1 || S.bottom - r.bottom < opts.story.bottom - 1)) {
        add(idx, 'error', 'story-ui-zone', `"${snippet}" sits under Instagram's Story UI (top ${opts.story.top}px / bottom ${opts.story.bottom}px).`);
      } else if (r.left - S.left < side - 1 || S.right - r.right < side - 1 || r.top - S.top < m - 1 || S.bottom - r.bottom < m - 1) {
        add(idx, isCover ? 'warn' : 'error', 'safe-zone', `"${snippet}" sits inside the ${isCover ? side : m}px edge margin${isCover ? ' (profile-grid crop zone)' : ''}.`);
      }
      const large = size >= 24 || (bold && size >= 18.66);
      const need = large ? 3 : 4.5;
      const cr = ratio(parse(cs.color).slice(0, 3), bgOf(el));
      if (cr < need) add(idx, 'error', 'contrast', `"${snippet}" contrast ${cr.toFixed(2)}:1 (needs ${need}:1).`);
      const isMeta = el.closest('.foot, .top, .source, .kicker, .rail, .cta-card, .d-label, th, .g-sign');
      if (!isMeta && size < opts.minFont) add(idx, 'warn', 'small-type', `"${snippet}" is ${Math.round(size)}px; under ${opts.minFont}px is hard to read on a phone.`);

      // glyph coverage: a char the font lacks falls back, so widths differ between two fallbacks
      const fam = cs.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
      const font = `${cs.fontStyle} ${cs.fontWeight} 80px "${fam}"`;
      if (!fontCache.has(font)) {
        ctx.font = `${font}, monospace`; const a = ctx.measureText('abcxyz').width;
        ctx.font = `${font}, serif`; const b = ctx.measureText('abcxyz').width;
        fontCache.set(font, Math.abs(a - b) < 0.01);
        if (Math.abs(a - b) >= 0.01) add(idx, 'error', 'font-missing', `Font "${fam}" did not load; the slide is rendering in a fallback font.`);
      }
      if (!fontCache.get(font)) return;
      for (const ch of new Set(el.textContent.replace(/\s/g, ''))) {
        // ASCII is always covered; arrows, checks and dashes are decoration a fallback draws fine
        if (/[\x21-\x7E→✓✕•—–“”«»…·]/.test(ch)) continue;
        ctx.font = `${font}, monospace`; const a = ctx.measureText(ch).width;
        ctx.font = `${font}, serif`; const b = ctx.measureText(ch).width;
        if (Math.abs(a - b) >= 0.01) {
          const k = `${fam}|${ch}`;
          if (!missingGlyph.has(k)) { missingGlyph.set(k, true); add(idx, 'error', 'missing-glyph', `Font "${fam}" has no "${ch}" glyph; it renders in a fallback font. Pick a font that covers the language.`); }
        }
      }
    });
  });
  return issues;
}

// ---------- render ----------

async function renderOne({ browser, spec, brand, theme, W, H, outDir, noPdf, quiet, jpeg }) {
  const baseCss = fs.readFileSync(path.join(THEMES_DIR, '_base.css'), 'utf8');
  const themeCss = fs.readFileSync(path.join(THEMES_DIR, `${theme}.css`), 'utf8');
  const tdef = THEMES[theme];
  const local = new Set(brand.fontFiles.map(f => f.family));
  const fams = [...new Set([brand.fonts.heading || tdef.fonts.heading, brand.fonts.body || tdef.fonts.body,
    brand.fonts.display || tdef.fonts.display, brand.fonts.mono || tdef.fonts.mono].filter(Boolean))].filter(x => !local.has(x));
  const { css: fontCss, missing } = await googleFontCss(browser, fams);

  fs.mkdirSync(outDir, { recursive: true });
  if (spec.palette || spec.tone === 'remembrance') {
    const colors = { ...brand.colors, ...(spec.palette || {}), ...(spec.tone === 'remembrance' ? REMEMBRANCE_PALETTE : {}) };
    for (const [k, v] of Object.entries(colors)) if (!hexToRgb(v)) die(`Palette colour "${k}" must be hex, got "${v}"`);
    if (!(spec.palette && spec.palette.accentInk) && spec.tone !== 'remembrance') colors.accentInk = inkFor(colors.accent);
    brand = { ...brand, colors };
  }
  const html = buildHtml({ spec: JSON.parse(JSON.stringify(spec)), brand, theme, themeCss, baseCss, fontCss, W, H });
  const htmlPath = path.join(outDir, 'carousel.html');
  fs.writeFileSync(htmlPath, html);

  const page = await browser.newPage({ viewport: { width: W + 80, height: H + 80 }, deviceScaleFactor: 1 });
  await page.goto('file://' + htmlPath, { waitUntil: 'load' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
  });
  const broken = await page.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src));

  let issues = copyChecks(spec);
  if (spec.tone === 'remembrance') issues.push({ slide: 0, level: 'info', code: 'tone-palette', msg: 'Remembrance palette applied (dark, sober). Brand colours are set aside for this post.' });
  for (const fam of missing) issues.push({ slide: 0, level: 'warn', code: 'font-fetch', msg: `Could not fetch "${fam}" from Google Fonts (offline or not a Google font). Add it under fonts.files in the brand kit.` });
  for (const src of broken) issues.push({ slide: 0, level: 'error', code: 'image-broken', msg: `Image failed to load: ${src}` });
  issues = issues.concat(await page.evaluate(pageQa, { minScale: 0.62, safe: 64, coverSide: 120, minFont: 26, story: H / W >= 1.7 ? STORY_SAFE : null }));

  // Save the fitted state so carousel.html matches the PNGs when opened by hand.
  fs.writeFileSync(htmlPath, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML));

  const slides = await page.$$('.slide');
  const files = [];
  for (let i = 0; i < slides.length; i++) {
    // The Instagram publishing API accepts JPEG only; --jpeg writes upload-ready files.
    const f = path.join(outDir, `slide-${pad2(i + 1)}.${jpeg ? 'jpg' : 'png'}`);
    await slides[i].screenshot(jpeg ? { path: f, type: 'jpeg', quality: 92 } : { path: f });
    files.push(f);
  }
  if (!noPdf) {
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.join(outDir, 'carousel.pdf'), width: `${W}px`, height: `${H}px`, printBackground: true, preferCSSPageSize: true });
    await page.emulateMedia({ media: 'screen' });
  }
  await page.close();
  await contactSheet(browser, files, path.join(outDir, 'contact-sheet.png'), W, H, `${spec.title || 'carousel'} · ${theme}`);

  const rank = { error: 0, warn: 1, info: 2 };
  issues.sort((a, b) => rank[a.level] - rank[b.level] || a.slide - b.slide);
  const report = { theme, size: `${W}x${H}`, slides: files.length, errors: issues.filter(i => i.level === 'error').length,
    warnings: issues.filter(i => i.level === 'warn').length, issues, files: files.map(f => path.basename(f)) };
  fs.writeFileSync(path.join(outDir, 'qa.json'), JSON.stringify(report, null, 2));
  if (!quiet) printReport(report, outDir);
  return report;
}

async function contactSheet(browser, files, out, W, H, label) {
  const cols = Math.min(files.length, 5), tw = 300, th = Math.round(tw * H / W);
  const cells = files.map((f, i) => `<figure><img src="file://${esc(f)}"><figcaption>${i + 1}</figcaption></figure>`).join('');
  const html = `<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:32px;background:#e9e7e2;font:600 18px/1.2 Inter,Arial,sans-serif;color:#222;width:max-content}
h1{font-size:20px;margin:0 0 20px}.g{display:grid;grid-template-columns:repeat(${cols},${tw}px);gap:20px}
figure{margin:0}img{width:${tw}px;height:${th}px;display:block;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,.18)}
figcaption{margin-top:8px;font-size:15px;color:#555}</style><h1>${esc(label)}</h1><div class="g">${cells}</div>`;
  const p = path.join(path.dirname(out), '.contact.html');
  fs.writeFileSync(p, html);
  const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
  await page.goto('file://' + p, { waitUntil: 'load' });
  await page.screenshot({ path: out, fullPage: true });
  await page.close();
  fs.unlinkSync(p);
}

function printReport(r, outDir) {
  const icon = { error: '✗', warn: '!', info: '·' };
  console.log(`\n${r.errors ? '✗' : '✓'} ${r.slides} slides · ${r.theme} · ${r.size} → ${outDir}`);
  for (const i of r.issues) console.log(`  ${icon[i.level]} ${i.slide > 0 ? `slide ${i.slide}` : 'carousel'}: ${i.msg}`);
  if (!r.issues.length) console.log('  QA clean.');
  console.log(`  ${r.errors} error(s), ${r.warnings} warning(s). Files: ${r.files[0]}..${r.files[r.files.length - 1]}${fs.existsSync(path.join(outDir, 'carousel.pdf')) ? ', carousel.pdf' : ''}, contact-sheet.png, qa.json`);
}

// ---------- main ----------

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.listThemes) {
    for (const [k, v] of Object.entries(THEMES)) console.log(`${k.padEnd(10)} ${v.description}`);
    return;
  }
  if (args.init) {
    const dir = path.resolve(args.init);
    fs.mkdirSync(path.join(dir, 'brands'), { recursive: true });
    const copies = [['example-carousel.json', 'carousel.json'], ['brand-kit.example.json', 'brands/my-brand.json']];
    for (const [src, dst] of copies) {
      const to = path.join(dir, dst);
      if (fs.existsSync(to)) { console.log(`  skip ${dst} (exists)`); continue; }
      let txt = fs.readFileSync(path.join(EXAMPLES_DIR, src), 'utf8');
      if (dst === 'carousel.json') txt = txt.replace('"brand": "brand-kit.example.json"', '"brand": "brands/my-brand.json"');
      fs.writeFileSync(to, txt);
      console.log(`  wrote ${to}`);
    }
    const rel = p => { const r = path.relative(process.cwd(), p); return r.startsWith('..') ? p : r; };
    console.log(`\nEdit brands/my-brand.json and carousel.json, then:\n  node ${rel(__filename)} ${rel(path.join(dir, 'carousel.json'))}`);
    return;
  }

  const specPath = args._[0] && path.resolve(args._[0]);
  if (!specPath) die('Usage: node build-carousel.cjs <spec.json> [--brand kit.json] [--theme name|all] [--size portrait|square|WxH] [--out dir] [--no-pdf]\n       node build-carousel.cjs --init <dir> | --themes');
  const spec = readJson(specPath, 'Carousel spec');
  const specDir = path.dirname(specPath);
  const brand = loadBrand(spec, specDir, args.brand);
  validateSlides(spec, specDir);
  const [W, H] = resolveSize(args.size || spec.size);
  const theme = args.theme || spec.theme || 'minimal';
  if (theme !== 'all' && !THEMES[theme]) die(`Unknown theme "${theme}". Themes: ${Object.keys(THEMES).join(', ')}, or all`);
  const outDir = path.resolve(args.out || path.join(specDir, 'out', path.basename(specPath, '.json')));

  let chromium;
  try { ({ chromium } = require('playwright')); } catch (_) {
    die('Playwright is not installed. Run: npm i -g playwright && npx playwright install chromium');
  }
  const browser = await chromium.launch();
  try {
    if (theme !== 'all') {
      const r = await renderOne({ browser, spec, brand, theme, W, H, outDir, noPdf: args.noPdf, jpeg: args.jpeg });
      process.exitCode = r.errors ? 1 : 0;
    } else {
      // Same copy in every theme, side by side, so picking a look is one glance.
      const sheets = [];
      for (const t of Object.keys(THEMES)) {
        const r = await renderOne({ browser, spec, brand, theme: t, W, H, outDir: path.join(outDir, t), noPdf: true, quiet: true });
        console.log(`${r.errors ? '✗' : '✓'} ${t.padEnd(10)} ${r.errors} error(s), ${r.warnings} warning(s)`);
        sheets.push([t, path.join(outDir, t, 'slide-01.png'), path.join(outDir, t, 'slide-02.png')]);
      }
      const cells = sheets.map(([t, a, b]) => `<figure><div>${[a, b].filter(fs.existsSync).map(f => `<img src="file://${esc(f)}">`).join('')}</div><figcaption>${t}</figcaption></figure>`).join('');
      const p = path.join(outDir, '.themes.html');
      fs.writeFileSync(p, `<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:32px;background:#e9e7e2;font:700 22px Inter,Arial,sans-serif;width:max-content}
.g{display:grid;grid-template-columns:repeat(3,auto);gap:28px}figure{margin:0}figure div{display:flex;gap:8px}
img{width:240px;display:block;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,.18)}figcaption{margin-top:10px}</style><div class="g">${cells}</div>`);
      const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
      await page.goto('file://' + p, { waitUntil: 'load' });
      await page.screenshot({ path: path.join(outDir, 'themes.png'), fullPage: true });
      fs.unlinkSync(p);
      console.log(`\nCompare: ${path.join(outDir, 'themes.png')}`);
    }
  } finally {
    await browser.close();
  }
}

main().catch(e => die(e.stack || e.message));
