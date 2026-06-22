# HOW_AGENT_MAKE_ONEPAGER.md

A complete operating manual for an AI agent that distills a whole presentation deck
into a single, dense, beautiful A4 PDF handout (the pattern built for
`ges_ai_workshop`, and reusable for any deck project such as `21_ai_academia`,
`23_ai_skoleni_ges`, `34_shape_agent`).

This is the companion to `HOW_AGENT_MAKE_SLIDES.md`. Slides are one-idea-per-screen for
a projector; a one-pager is the opposite discipline: the **entire workshop on one
sheet**, audience-facing, printed or downloaded, read at arm's length. Read this fully
before generating or editing a one-pager.

Writing convention for this file and all one-pager copy: no em dash characters. Use
colons, commas, parentheses, or restructure. (En dash only for numeric ranges.)

---

## 0. The one sentence

One A4 page that distills an entire deck for the audience to take away: a gradient
header, a "big idea" band, a 3-column grid of tight cards with small in-style SVG
diagrams, and a full-width strategy band at the bottom, every number sourced and
fact-checked, rendered to a single-page PDF whose footnote is stamped with the
generation time and the commit hash, and wired to a download button on the web.

This is the inverse of a slide: a slide removes detail to the notes; a one-pager
**compresses** the whole story onto one face, but stays clear, not crammed.

---

## 1. Non-negotiable principles

1. **One page, always.** The deliverable is exactly one A4 page. Not 1.2, not 2. If it
   does not fit, you distill harder or tune density, you never spill to a second page.
   Verify the page count of the produced PDF every time (section 7.3).
2. **Distill, do not dump.** The deck has 100+ slides; the one-pager carries the spine:
   the few stats that matter, the tool landscape, the chat-to-agent shift, the security
   and regulation core, the everyday use-cases, and the deployment strategy. Extract the
   most important, drop the rest. "Condensed but not tiny" (see 2).
3. **Audience-facing only.** No speaker notes, no lecturer commentary, no AI or meta
   remarks, no internal client framing. If the deck has `notes-data` (lecturer notes),
   strip them before reading. The sheet is what a participant keeps.
4. **Condensed, but readable.** Dense is fine; microscopic is not. Body copy floor is
   about `6.7pt` to `7.2pt` for a one-pager handout (read at 30 to 50 cm, not from a
   hall). Headers `8` to `10pt`, the title `~18pt`. Below ~6.5pt is too small.
5. **Match the deck exactly.** Reuse the deck's design tokens verbatim (the orange ramp,
   Inter Tight / Source Serif 4 / JetBrains Mono). The one-pager must look like it came
   from the same family. Self-contained CSS (no dependency on the deck's stylesheet) so
   the PDF renders standalone.
6. **Every number is sourced and true.** Each stat carries a short source in brackets
   (the report name, not a link), estimates are labelled as estimates ("až -50 %, odhad"),
   and the whole sheet is fact-checked against the web before it ships (section 9). Truth
   in materials: only what is real.
7. **Fill the page, balanced.** No blank ocean at the bottom and no lopsided columns.
   Columns end at the same height; the bottom is anchored by a full-width band. Use the
   measurement loop (section 6) to make this exact, not eyeballed.
8. **Diagrams are small and in-style.** Reuse the deck's diagram vocabulary as compact
   inline SVG: the agent loop, a small pyramid, a 30/60/90 timeline, a risk strip, a
   left-to-right flow. They carry "beautiful diagrams" without raster clutter.
9. **Illustrations: white-stroke SVG on color, keyed raster on light.** A raster
   illustration with a white background dropped on the orange header reads as a white box
   with low contrast. On a colored header use a white-line SVG motif instead. (This was a
   real fix: the first header art had a visible white background and no contrast.)
10. **Breathing room, and no gratuitous line breaks.** Every cell keeps its padding and
    the grid keeps its gaps; nothing touches a neighbour or the page edge (cells must
    breathe). Do not let text wrap when its row still has horizontal room: short text
    stays on one line. A wrap that strands one or two words on the next line (an orphan)
    is a defect, tighten the copy, widen the box, or use a non-breaking space. Extra lines
    or wraps are acceptable ONLY when you are deliberately spending them to fill vertical
    space and there is no better option (and even then, prefer a real content line over a
    ragged orphan). A real example: when the footer punchline wrapped to two ragged lines,
    the fix was to give it its own full-width row so it sits on ONE line, and spend the
    freed vertical space as a clean gap above the strategy band, not as an ugly wrap.
    **Widows and orphans (Czech typography).** Never let a single-letter preposition
    (`k s v z o u`) or conjunction (`a i`) sit at the END of a line, and never strand an
    opening bracket plus preposition (`(v` at a line end is wrong). Tie them to the next
    word with a non-breaking space (`&nbsp;` / U+00A0), e.g. `(v&nbsp;produkci`. Do the
    same for a number and its unit (`20&nbsp;%`, `35&nbsp;mil.`). The non-breaking space
    is the correct fix, NOT a manual `<br>` (which breaks at the wrong place at other
    widths). Real example: the 77 % stat label wrapped as "...AI (v" at the line end, and
    was fixed with `(v&nbsp;produkci`.

---

## 2. Technical foundation (copy this skeleton)

A one-pager is **physical print geometry**, not a scaled stage. Author in millimetres at
true A4, and let the browser's print engine map it 1:1 to the PDF page.

```css
:root{
  /* identical tokens to the parent deck */
  --c-1:#ff5a1f; --c-2:#ff8a1f; --c-3:#ff3b1f;
  --accent-soft:#fff3ec; --accent-line:#ffd9c4;
  --paper:#ffffff; --paper-soft:#fbfaf7;
  --ink:#0e0e10; --ink-2:#3a3a40; --ink-3:#6b6b73; --rule:#e6e6ea;
  --display:"Inter Tight",system-ui,sans-serif;   /* headings/UI */
  --serif:"Source Serif 4",Georgia,serif;          /* body */
  --mono:"JetBrains Mono",ui-monospace,monospace;  /* kickers/footnotes/sources */
}
.sheet{ width:210mm; height:297mm; overflow:hidden;
  padding:6.5mm 7.5mm 5.5mm; display:flex; flex-direction:column }
@page{ size:A4; margin:0 }
@media print{ html,body{background:#fff} .sheet{box-shadow:none} }
```

Key choices:

- **Units are `mm` and `pt`, not `cqw`.** Slides use container-query units because they
  scale to any screen; a one-pager has one fixed physical size, so use real print units.
  This makes the on-screen preview and the PDF identical.
- **`@page{size:A4;margin:0}` plus `preferCSSPageSize`** in the renderer (section 7) so
  the PDF page is exactly A4 with no engine margin. The `.sheet` is the full page; its
  internal padding is the print margin.
- **`overflow:hidden` on `.sheet`** is a guard, not a strategy. If content overflows,
  fix the content; do not rely on the clip (it hides bugs, see section 6).
- **Flex column layout:** header (fixed), big-idea band (fixed), columns grid (grows),
  strategy band (fixed), footer (fixed). Only the columns grid flexes.

Type scale that read well on the real sheet (A4, dense handout):

| role                 | size       |
|----------------------|------------|
| title h1             | `18pt`     |
| big-idea band        | `9pt`      |
| card heading (h2)    | `8.2pt`    |
| card body / li       | `6.7pt`, line-height `1.2` |
| card sub (italic)    | `6.5pt`    |
| stat number          | `10pt`     |
| source line (mono)   | `5.4pt`    |
| footnote / stamp     | `5.6pt`    |
| strategy band title  | `9.6pt`    |

These are the floor for a handout, not a projector. If text this size will not fit, you
have too much content: distill, do not shrink below ~6.5pt.

---

## 3. Layout: header, big idea, 3 columns, full-width band, footer

The proven structure, top to bottom:

1. **Header** (orange gradient, rounded): mono kicker, big title with one gradient word
   (white on the orange, see 9), one-line italic lead, and a meta row (terms, time,
   place) pulled from the deck's `program.json` / title slide. A white-stroke SVG motif
   sits in the top-right corner.
2. **Big-idea band:** one bold sentence, the thesis of the day, in an accent-soft strip
   with a left orange border. This is the deck's opening statement.
3. **Columns:** a `1fr 1fr 1fr` grid. Each column is a flex column of 3 cards. Cards are
   `.card` (soft background, thin rule, rounded), each with an icon + heading, optional
   italic sub, a tight bullet list, and a small mono **source line** in brackets.
4. **Strategy band (full width):** the conclusion spans all three columns at the bottom,
   filling what would otherwise be blank. Internally a 4-column grid: a small pyramid
   ("stavte zdola nahoru"), the success principles, a 30/60/90 timeline, and an action
   callout (the "champion" + a closing quote). This was added specifically to fill the
   bottom and anchor the page.
5. **Footer:** a one-line punchline + a credit line on the left, the generation stamp on
   the right.

Compact components reused from the deck (built small, in mm):

- `.stats` row: 3 tiles, each a big gradient number + tiny label.
- `.flow`: chat to agent boxes with arrows.
- `.loop`: the agent loop (plan, act, verify, repeat) as 3 nodes + a recycle glyph.
- `.duo`: a one or two box mini-compare ("do AI NEDAVAT").
- `.risk`: the EU AI Act 4-tier strip (color bar + label per row).
- `.pyr`: a 3-tier SVG pyramid (orange ramp, dark text on light tiers, white on dark).
- `.tline`: the 30/60/90 phases.

---

## 4. Source the content from the deck, not from memory

The one-pager must be built from the **actual current deck**, not from what you remember
a similar deck said. Decks drift (models, dates, numbers, new blocks).

1. Find the source of truth. For a multi-file deck it is `blocks/<NN>/<NN>-*.html`
   (one slide per file), `program.json` (title, subtitle, time, place, terms, schedule),
   and `shared/`. For a single-file deck it is the one HTML.
2. Extract audience-facing text programmatically: strip `notes-data` (lecturer notes) and
   `<svg>`, then pull kicker, heading, lead, list `<strong>` titles, stat numbers, and
   source footnotes per slide. Dump it to a file and read it.
3. Confirm exact figures from the slides that carry them (do not assume from an older
   deck). Example real differences caught this way: "280x **za 2 roky**" (not 18 months),
   downtime cost "1,4 bil. USD/rok" (the deck had already fixed an older wrong figure),
   "82 % zvyšuje rozpočet", model lineup "Opus 4.8 / GPT-5.5 / Gemini 3.5".
4. Pull the header meta and contacts from `program.json` and the closing slide, so the
   sheet matches the live web exactly.

Extraction sketch:

```js
let body = html.replace(/<aside class="notes-data">[\s\S]*?<\/aside>/g,'')   // drop lecturer notes
               .replace(/<svg[\s\S]*?<\/svg>/g,'');
const clean = s => s.replace(/<[^>]+>/g,' ').replace(/&[a-z]+;/g,' ').replace(/\s+/g,' ').trim();
// then per slide: kicker, h1/h2, .lead, <strong>..</strong>, .kpi-num / .n
```

---

## 5. The PDF render and the footer stamp

Render with Playwright's `page.pdf()`. Generate it as a **pregenerated, committed
artifact**, because the deploy host (Vercel) only runs the deck build, not a headless
browser. The build step copies it into the output.

```js
import { chromium } from 'playwright';
import { execSync } from 'child_process';

const commit = execSync('git rev-parse --short HEAD').toString().trim();
const stamp  = new Intl.DateTimeFormat('cs-CZ',{ timeZone:'Europe/Prague',
  day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit' })
  .format(new Date()).replace(',','');   // Date.now is fine here; not a workflow

const page = await browser.newPage();
await page.goto('file://'+SRC, { waitUntil:'networkidle' });
await page.evaluate(() => document.fonts.ready);          // fonts MUST be ready
await page.evaluate(({stamp,commit}) => {                 // stamp the footnote
  document.getElementById('gen').innerHTML =
    'Vygenerováno a zkontrolováno ' + stamp + ' &middot; v1 (' + commit + ')';
}, {stamp, commit});
await page.pdf({ path:OUT, width:'210mm', height:'297mm',
  printBackground:true, preferCSSPageSize:true, pageRanges:'1',
  margin:{top:'0',right:'0',bottom:'0',left:'0'} });
```

Footnote rules (audience-facing, subtle, bottom-right, mono ~5.6pt):

- **Generation time** in the local (Prague) timezone, human format.
- **Commit hash in brackets** as a quiet internal version marker: `(9141fce)`. The
  audience does not need to decode it; you do, to know which version is in someone's hand.
  Note the inherent off-by-one: the PDF is built before the commit, so the stamp shows
  the parent commit. That is fine as a version reference.
- `await document.fonts.ready` before rendering, or the PDF ships with fallback fonts.
- `pageRanges:'1'` is a final guard against a stray second page.

---

## 6. The fit-to-one-page loop (the heart of it)

This is the part that takes the iterations. You cannot eyeball one-page fit; measure it
with Playwright and tune until the numbers are right.

### 6.1 What to measure

Render the page (not the PDF) and compute, in mm (`mm = px / 3.7795` at 96 dpi):

- `scrollHeight` vs `clientHeight` of `.sheet`. They must be equal (no page overflow).
  But beware: **overlap does not show up as overflow** (overlapping elements do not add
  height), so this check alone is not enough.
- The **slot** available to the columns = `strip.top - cols.top - (cols-to-strip margin)`.
- Each column's **natural content height** = sum of its card heights + inter-card gaps.
  Every column must be `<= slot`, or it overlaps the band below.
- An explicit **overlap probe**: for each card, is `card.bottom > slotBottom + tolerance`?
  Collect the offenders by heading.

```js
const mm = px => +(px/3.7795).toFixed(1);
const slotBottom = strip.getBoundingClientRect().top - cols2stripMarginPx;
let overlap = [];
document.querySelectorAll('.card').forEach(c => {
  if (c.getBoundingClientRect().bottom > slotBottom + 1.5)
    overlap.push(c.querySelector('h2')?.textContent.slice(0,16));
});
```

### 6.2 Equal-height columns without overlap

To make all three columns end at the same height (the "fill the page, balanced" goal):

1. First ensure **every column's content is `<= slot`** (trim or shrink type until it is).
2. Then set `.col{ display:flex; flex-direction:column; justify-content:space-between }`.
   With positive free space, the cards spread and all columns' bottoms align exactly at
   the slot bottom. Verify the measured `colBottoms` are identical.

Critical failure mode: `justify-content:space-between` with content **larger** than the
slot produces **negative free space**, which makes cards overlap (and overlap is
invisible to the overflow check). So space-between is only safe after step 1. If you see
overlap, the column is too tall; trim, do not rely on the clip.

### 6.3 How to tune density

In order of preference:

1. Distill content (fewer bullets, merge lines). Always first.
2. Shrink the whole card type a notch (e.g. body `7.2pt` to `6.7pt`, line-height `1.24`
   to `1.2`, gaps down). A ~10% type reduction buys ~10% height.
3. Tighten the strategy band a few mm to give the columns more slot.
4. Give one column more or fewer cards to balance, or move a card between columns.

Lesson learned: it is easy to **over-enrich**. When asked to "fill" columns 2 and 3, the
first pass added too much and pushed them past the slot (164mm and 169mm into a 158.8mm
slot), causing overlap. The fix was: add genuinely useful content (source lines, one or
two real deck points), then trim back below the slot, then let `space-between` align the
bottoms. Add with intent, measure, trim to fit.

---

## 7. Build, integrate, deploy

### 7.1 Where the files live

- `onepager.html` (source, self-contained), `build-onepager.mjs` (renderer), and the
  output `media/onepager.pdf` at the repo root. The output goes under `media/` because a
  multi-file deck's build already copies `media/` into `dist/`.
- Add an `npm run onepager` script. Vercel does **not** run it (it only runs the deck
  build); the PDF is committed and copied as a static asset.

### 7.2 The download button

Add a download button next to an existing control (for `ges_ai_workshop` it sits beside
the "Rozbalit vše" button generated in `build.mjs`). Use a styled anchor with a
`download` attribute and a friendly filename:

```html
<a id="onepagerBtn" href="media/onepager.pdf"
   download="GES-AI-workshop-onepager.pdf">&darr; One-pager (PDF)</a>
```

Style it as a secondary (soft) button so it reads as a companion to the primary action.

### 7.3 Verify and ship

- Page count is exactly 1: count `/Type /Page` objects in the PDF, or rely on
  `pageRanges:'1'` plus the measured `scrollHeight == clientHeight` and empty overlap set.
- Regenerate the PDF, then run the deck build so `dist/media/onepager.pdf` updates.
- Respect the project's push rule. `ges_ai_workshop` requires explicit user approval for
  every push to `master` (it auto-deploys). Commit freely; push only when asked.
- Wrap heavy local commands per the host rule (here, prefix one-off node/git with
  `CC_BUILD_SKIP=1` if the build guard misfires on a light command).

---

## 8. Diagrams (small SVG, in the orange ramp)

Same idea as the deck's diagrams, sized down to mm. Build SVG polygons in the orange ramp
(`#ffd9c4`, `#ff9e6b`, `#ff5a1f`), dark text (`#7a3a18`) on light tiers, white on dark.
Keep them tiny but legible: a 3-tier pyramid ~30mm wide, a 4-node loop, a 3-cell
timeline. Do not invent new diagram styles; shrink the ones the deck already uses so the
sheet stays in-family.

---

## 9. Fact-check and proofread before shipping

### 9.1 Fact-check every claim (web, adversarial)

Every number and named fact on the sheet gets verified against the web. Spin a few
subagents in parallel, each taking a slice (science/breakthroughs, economics/adoption,
safety/regulation), each web-searching and returning a verdict per claim
(CONFIRMED / PARTIALLY / CONTRADICTED / UNVERIFIABLE) with the correct value and a
source URL. Rules that matter:

- Do not assert something is false from memory; 2026-dated items may be after your
  cutoff. Search first; mark "UNVERIFIABLE via search" rather than declaring false.
- Separate **sheet-level** from **deck-level** issues. The corrections that matter are
  the ones on the one-pager; report the rest as deck follow-ups.
- Apply the outcome: correct wrong values, **qualify estimates** ("až -50 %, odhad"),
  fix attributions (e.g. the Czech EU AI Act supervisor is ČTÚ, not MPO), and add short
  **source lines in brackets** (`// zdroje: Rootstock, McKinsey, Stanford AI Index 2026`),
  not links.

### 9.2 Proofread the language with a top model

Run the visible text through a strong language model (the workshop's stated model, e.g.
GPT-5.5; verify the current id, do not assume from memory) as a native proofreader. Ask
for a JSON list of `{original, fix, why}` for genuine errors only (grammar, missing
commas, unnatural phrasing, diacritics), keeping terminology and the no-em-dash rule.
Apply the legitimate fixes; skip extraction artifacts. Pass any API key only via an env
var, never commit it, and remind the user to rotate a key shared in plaintext.

Real fixes this caught in Czech: "nejde o jestli" to "nejde o to, jestli"; missing commas
before subordinate clauses; "az" to "až" (diacritics); "mil." with a period; agreement
("1 z 5 firem zažila").

---

## 10. Pitfalls (all hit and fixed in the real build)

1. **Header raster art on color = white box, low contrast.** Replace with a white-stroke
   SVG motif on the gradient. Keyed raster art is for light surfaces only (same rule as
   the slides manual).
2. **Blank bottom of the page.** Make the conclusion a full-width band spanning all
   columns; it both fills the void and gives the page a strong anchor.
3. **Over-enriching columns into overlap.** `space-between` hides overflow as overlap.
   Always re-measure after adding; keep every column `<= slot`.
4. **Context-free big numbers.** A bare "2,6 az 4,4 bil. USD" means nothing to a reader.
   Either give it a clear frame or cut it. Prefer fewer, clearer numbers.
5. **Assuming content from a sibling deck.** Always read the current blocks; figures and
   model names drift.
6. **Footer stamp without fonts ready.** Await `document.fonts.ready` or the PDF embeds
   fallback glyphs.
7. **Forced wraps and stranded words.** Cramming a long line into a narrow box makes it
   wrap with one or two words orphaned on the next line, which looks broken. Give long
   content its own full-width row (the footer punchline fix), tighten the copy, or widen
   the cell. Keep padding and gaps so cells breathe. Wrap only to fill space on purpose,
   never by accident.

---

## 11. Pre-ship checklist

1. Exactly one A4 page (page count verified; `scrollHeight == clientHeight`; overlap set
   empty).
2. Columns balanced: all three bottoms aligned, no blank ocean, full-width band anchors
   the bottom.
3. Body type `>= 6.5pt`, readable at arm's length; nothing crammed; cells have padding
   and gaps (they breathe); no wrap strands one or two words on the next line (orphan),
   short text stays on one line.
4. Looks like the parent deck: same tokens, fonts, orange ramp, diagram vocabulary.
5. Audience-facing only: no lecturer notes, no AI/meta text.
6. Every number sourced (short bracketed source), estimates labelled, all facts
   web-verified; corrections applied.
7. Language proofread by a strong model; no em dashes; diacritics correct.
8. Header motif is a white-stroke SVG on the colored header (good contrast).
9. Footer stamped with generation time + commit hash in brackets; fonts embedded.
10. PDF committed under `media/`, copied into `dist/` by the build, download button wired
    next to an existing control with a friendly `download` filename.
11. Deck build re-run; push only with the project's required approval; live URL checked.

---

Sources that informed this manual: the `ges_ai_workshop` one-pager build (A4 mm layout,
the fit-to-one-page measurement loop, the full-width strategy band, the white-stroke
header motif, the Playwright PDF render and footer stamp, the subagent fact-check and the
GPT-5.5 Czech proofread), and its companion `HOW_AGENT_MAKE_SLIDES.md` (tokens,
component vocabulary, illustration and verification philosophy).
