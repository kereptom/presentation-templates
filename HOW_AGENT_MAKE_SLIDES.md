# HOW_AGENT_MAKE_SLIDES.md

A complete operating manual for an AI agent that generates research grade,
visually beautiful presentation decks as self contained HTML (the pattern used in
`21_ai_academia`, `23_ai_skoleni_ges`, `34_shape_agent`, and future deck projects).

This file is the single source of truth. Read it fully before generating or editing
any slide. It covers: the design principles, the technical foundation, the layout and
component system, the illustration pipeline (Nano Banana Pro / 2), the writing rules,
and the Playwright + Gemini vision verification loop that you must run until the deck
passes.

Writing convention for this file and for all slide copy: no em dash characters. Use
colons, commas, parentheses, or restructure. (En dash only for numeric ranges.)

---

## 0. The one sentence

Every slide carries one idea, stated in a few large bold words, supported by either a
purpose built component (cards, KPIs, a chart, a diagram) or one well placed
illustration, with generous and intentional whitespace, and it is verified by a vision
model before it ships.

---

## 1. Non negotiable principles (the "why it looks good")

1. **Core ideas on the face, all detail in the speaker notes.** This is the general
   workflow for every deck. A slide is not a document. Put only the core idea on the
   slide (a headline plus at most 3 short lines, each a few words). Every supporting
   specific, citation, number, repo, and nuance goes into the speaker notes that sit
   under the slide. One idea per slide: if a slide carries two ideas, or will not fit at
   a readable size, SPLIT it into more slides. Never delete information to make room;
   move it into the notes. More short slides beat one dense slide.
2. **Projector legibility is mandatory.** Assume the back of a large room and a dim
   projector. On screen body text must be large: minimum about 24px at the 1280px stage
   (roughly 1.9cqw), bullets 24 to 26px, and never below 20px for anything the audience
   must read. If larger text causes overflow, the slide has too much on it: compact the
   face and move detail to notes, or split the slide. Auto fit (scaling a slide down to
   fit) is a safety net, not a layout strategy: if a slide is being auto scaled below
   about 0.9, it is too full, fix the content, do not accept the shrink.
3. **High signal to noise (SNR).** Signal = the few words and the one visual that
   matter. Noise = everything else (decoration, redundant labels, tiny text in big
   empty boxes). Maximize the size of the signal, delete the noise. The most common
   failure is *small text inside a large empty container*: either the text grows to
   fill the container or the container shrinks to the text. Never leave a big box 70%
   empty with a 13px caption in it.
4. **Fill the canvas, but keep good proportions (no blank oceans AND no gangly
   columns).** Content should occupy most of the slide, not sit in a thin band with empty
   space above and below. BUT do not over correct by stretching a sparse grid to 100%
   height: a 2 up comparison or a single row of 4 KPIs stretched to the full height
   becomes ugly tall boxes with a few words floating in the middle. The right move:
   - Cards and KPI tiles get a sensible `min-height` (substantial presence) with content
     vertically centered inside, and the grid is `align-content:center` so it sits
     centered with balanced margins. They look like solid, well proportioned cards.
   - A full 2x2 of cards naturally fills most of the height; a 2 up or a KPI row sits
     centered with a little balanced whitespace, which is elegant, not broken.
   - Bullet lists DISTRIBUTE vertically (`flex:1; justify-content:space-evenly`) so 3 to
     5 bullets span the column.
   Balanced whitespace around a well sized element is good taste. Asymmetric blank (all
   at the bottom) and gangly full height boxes are both fails. If a void remains, the
   text is too small (grow it) or there is too little content (merge or add a visual).
5. **Whitespace is intentional, never accidental.** Empty space should frame and point
   at the signal. A tiny graphic stranded in a sea of blank is the worst case. Either
   give a visual real space as a focal element, or balance it against the text in a
   grid. (BrightCarbon, Design Shack 2025.)
6. **Proportional, not absolute.** Type and spacing scale with the slide using
   container query units (`cqw`), so a deck looks identical at any screen size and
   every slide shares one rhythm. Fixed pixels drift out of proportion.
7. **A small, strict design system beats per slide creativity.** One type scale, one
   color set, one spacing unit, a fixed library of layouts. Variety comes from the
   *content and the illustrations*, not from re inventing the grid each slide.
8. **Illustrations live in the layout, not on top of it.** An illustration is a grid
   column or a defined region with breathing room, not an absolutely positioned image
   that bleeds under the text. Overlapping text is an automatic fail.
9. **Bold typography is the main visual.** Big confident headlines (a single gradient
   accent on one or two words) do more than any clip art.
10. **Truth in materials.** Only claim what is built. Label proposals as proposals, cite
   every external system with a year. If any slide is forward looking, the web index
   must carry a visible disclaimer (see section 11).

---

## 2. Technical foundation (copy this skeleton)

**Fixed stage, scaled to fit.** Author everything inside a logical `1280 x 720` stage
(16:9). Scale the whole stage to the viewport with a CSS transform; never reflow slide
content to the window.

```html
<div class="stage">            <!-- visible frame, aspect-ratio:16/9, centered -->
  <div class="slides-host">    <!-- 1280x720, container-type:size, transform:scale(var(--scale)) -->
    <section class="slide active"> ... </section>
  </div>
</div>
```

```css
:root{
  /* color tokens: one ink ramp, one paper ramp, two brand accents, one rule */
  --paper:#ffffff; --paper-soft:#f6f8fb; --bg:#eef1f6;
  --ink:#0b1220; --ink-2:#33425a; --ink-3:#5d6c82; --rule:#e2e8f0;
  --c-1:#0e9bb5; --c-2:#13b6d4; --c-3:#c026a6;     /* cyan / cyan-light / magenta */
  --grad:linear-gradient(135deg,var(--c-2),var(--c-1) 55%,var(--c-3));
  --display:"Inter Tight",system-ui,sans-serif;     /* headlines */
  --serif:"Source Serif 4",Georgia,serif;           /* lead / quotes */
  --mono:"JetBrains Mono",ui-monospace,monospace;   /* kickers / labels / footers */
}
.slides-host{width:1280px;height:720px;container-type:size;container-name:stage;
  transform-origin:top left;transform:scale(var(--scale,1))}
.slide{position:absolute;inset:0;padding:5% 7%;display:none;flex-direction:column;justify-content:center}
.slide.active{display:flex}
```

**Type scale in `cqw`** (1cqw = 1% of stage width = 12.8px at 1280). These values come
from the reference deck and read well:

| role            | size        |
|-----------------|-------------|
| title h1        | `7.0–7.4cqw` |
| section h1      | `7.0cqw`    |
| slide h1 / h2   | `5.0cqw` / `3.4cqw` |
| statement big   | `4.5–5.0cqw` |
| body / li       | `2.0–2.1cqw` (>= 25px), never below 20px |
| lead (serif)    | `2.2–2.3cqw` |
| card title      | `2.3cqw` (>= 28px) |
| card body       | `1.9cqw` (>= 23px) |
| kicker / footer | `1.1–1.3cqw` (chrome, may be small) |
| KPI number      | `4.5cqw` (>= 56px) |
| KPI / axis label| `1.8cqw` (>= 22px) |

Components that fill the height (principle 4): card grids and KPI grids are vertically
centered (`align-content:center`) with each card a substantial `min-height` (about 200
to 240px) and `display:flex; flex-direction:column; justify-content:center` so content
sits in the middle of a well proportioned card. Do NOT use `grid-auto-rows:1fr` to
stretch a sparse 2 up or a single KPI row to full height: that makes gangly columns. A
full 2x2 fills most of the height on its own. Bullet lists use `flex:1;
justify-content:space-evenly` so 3 to 5 bullets distribute down the whole column. The
result is large, well proportioned cells and large text, which is what a 300 person hall
needs.

These are projector minimums, not maximums. Bigger is better as long as nothing
overflows. If text this size does not fit, the slide has too much content: compact the
face and move detail to the notes, or split into more slides (principles 1 and 2). Only
footers, page numbers, and diagram captions may go smaller, and they never carry content
the audience must read.

Line height: headlines `1.02–1.1`, body `1.4–1.5`. Body text `max-width` about `48–52ch`.
Outer padding `5% 7%` gives the guaranteed breathing margin. A global `--fs` multiplier
on the stage lets you nudge type per slide for auto fit.

If you are extending an existing px based generator (like `34_shape_agent`) rather than
starting fresh, you can keep px, but then you MUST hold the layout rules below (grid
based illustration, SVG text sized relative to its own viewBox). New projects: use
`cqw`.

### 2.1 Deck client runtime (nav, speaker notes, notes zoom)

The client script handles: arrow / space / tap navigation, `F` fullscreen, a progress
bar, and a speaker-notes overlay toggled with `N`. Carry these into every deck built on
this engine family.

**Notes zoom (persisted).** The presenter must be able to resize the speaker-notes text
on the fly and have it remembered. Pattern:

- Drive the notes panel font size from a CSS variable: `#notes{font-size:var(--note-fs,16px)}`
  (the `h4` header keeps its own fixed size so only the body scales).
- A sticky control top-right inside the panel with a `&minus;` button, the current size,
  and a `+` button (`data-z="-1"` / `data-z="1"`). Also bind `+`/`=` and `-`/`_` keys
  while the panel is open.
- On change: `el.style.setProperty('--note-fs', px+'px')`, clamp to `11–40px` (step 2),
  and `localStorage.setItem('noteFs', px)`. On load, read `noteFs` back and apply before
  first paint. Wrap localStorage in try/catch (private mode).
- The notes click handler must `stopPropagation()` so zoom clicks do not trigger
  tap-to-advance.

Reference implementation: `34_shape_agent/assets/deck.js` (`applyNoteFs` / `zoomNotes`)
and the `.note-zoom` rules in `assets/deck.css`.

---

## 3. Layout and component library

Pick the layout that fits the content. Do not force everything into bullets.

- **title**: kicker, big h1 (one gradient word), italic serif sub, mono byline. If it
  has an illustration, use the split grid (section 4), text left, art right.
- **section divider**: dark gradient background, big white h1 with one underlined or
  gradient word, optional one line lead, big section number. No illustration: dark
  dividers stay clean and typographic (see 5.3). The bold type and color carry them.
- **statement**: one short sentence at `4.5–5cqw`, vertically centered. Optional split
  with an illustration on the right.
- **bullets**: kicker + h2 across the top, then 3 to 5 short bullets. If illustrated,
  bullets go in the left column of a split, illustration right. Never more than 5
  bullets; if more, switch layout or split the slide.
- **two-col cards**: cards in a 2 column grid, each a bold title + 2 lines. An even
  count (2 or 4) fills cleanly. If the count is ODD (3, 5), do NOT leave the last card
  alone on the left with a dead quadrant beside it: CENTER the lonely last card on its
  row. CSS: `.cols .card:last-child:nth-child(odd){grid-column:1 / -1; justify-self:
  center; width:calc(50% - <half the gap>)}`. The orphan card then sits centered, one
  column wide, under the row above it.
- **kpi tiles**: 2 to 5 tiles, each a big gradient number + short label. Great for
  "what works" or metrics.
- **quote**: large italic serif, left accent border, attribution in mono.
- **diagram** (see section 8): pipeline, timeline, matrix 2x2, bars, pyramid. Use when
  structure (sequence, comparison, hierarchy) is the point.

Each non divider slide gets a slim footer (mono, `--ink-3`): deck short title left,
section right. Title and section slides have no footer.

---

## 4. The split grid (how to place an illustration next to text)

This is the rule that fixes the three classic faults: illustration under the title,
no breathing room, and tiny art in a blank slide.

```css
.split{display:grid;grid-template-columns:1.32fr 0.9fr;gap:6%;align-items:center;
  width:100%;flex:1;min-height:0}
.split.below{margin-top:1.5%}                 /* when a full width title sits above */
.split-text{min-width:0;display:flex;flex-direction:column;justify-content:center}
.split-art{display:flex;align-items:center;justify-content:center;height:100%}
.split-art img{max-width:100%;max-height:80%;object-fit:contain}  /* max-height = vertical breathing */
```

Rules:

- Text always in the left column, illustration in the right column. The `gap` is the
  inner breathing room; the slide padding is the outer breathing room. The art never
  touches an edge and never sits under text.
- For **bullets**, the title (kicker + h2) spans the full width on top, then a
  `.split.below` holds bullets (left) and art (right).
- For **title / statement / quote**, the whole content is the split.
- `max-height:80%` on the art keeps vertical breathing so a tall illustration does not
  fill the column edge to edge.
- Do not put illustrations on `two-col`, `kpi`, or `diagram` slides; they already carry
  their own visual. Adding art there is noise.

Default: illustrations go only on light slides. Dark section dividers carry NO
illustration. On a dark background the keyed line art tends to read as a misplaced,
poorly fitting figure rather than an ambient glow, so dividers stay clean and
typographic (big headline, one accent word, section number). If you ever want art on a
dark surface, design a dedicated dark composition for it, do not reuse the light slide
asset.

---

## 5. Illustration system

### 5.1 Model: use Nano Banana Pro, and verify the version every run

As of June 2026 the current Google image models are:

- **Nano Banana Pro = Gemini 3 Pro Image**, id `gemini-3-pro-image-preview`. Highest
  quality, reasoning, best for hero and key illustrations.
- **Nano Banana 2 = Gemini 3.1 Flash Image**, id `gemini-3.1-flash-image`. Fast and
  cheap, good for bulk spot illustrations.

**You must web search for the current model id at the start of every deck project.**
Model names move fast and your training data is stale. Search "latest Nano Banana /
Gemini image model id" and "latest Gemini Flash vision model", and update the scripts.
If the current best image model is from another vendor (for example a newer OpenAI
`gpt-image-*`, per the user's standing rule the OpenAI default is `gpt-image-2`, or a
strong open model), say so and offer to switch. Do not hardcode an old id silently.

Endpoint pattern (Gemini): `POST https://generativelanguage.googleapis.com/v1beta/models/<MODEL>:generateContent?key=$GEMINI_KEY`
with `{"contents":[{"parts":[{"text": prompt}]}]}`; read the image bytes from
`candidates[].content.parts[].inlineData.data` (base64). Never hardcode the key; read
it from an env var or a gitignored `.env`.

### 5.2 Generate on pure white, then key to transparent

Generate every illustration on a pure solid white background, then remove the white to
get a transparent PNG. A transparent asset reads correctly on BOTH light slides (full
ink and color) and dark dividers or headers (the dark ink recedes, the cyan and magenta
accents glow). This is more flexible than `mix-blend-mode:multiply`, which only works on
light backgrounds.

Keying (fast, vectorized, keeps anti aliased edges): `alpha = 255 - min(R,G,B)`. Pure
white becomes fully transparent; saturated color and dark ink stay opaque; light grays
become faint. Implementation (PIL): split RGB, `m = darker(darker(R,G),B)`,
`alpha = invert(m)`, merge RGBA. See `transparent.py` below.

### 5.3 Placement and sizing

- Content slide art (light slides only): a real grid column (section 4), roughly 0.9fr
  next to 1.32fr text.
- Section dividers (dark): no illustration. Typographic only.
- Web index header (dark): the one allowed dark-surface illustration, transparent,
  on the right of the title text, `opacity:1`, generated as a dark composition (luminous
  cyan and magenta lines, keyed black-to-transparent so the glow shows). Two things that
  matter and are easy to get wrong:
  - CROP the dead transparent margin off the PNG first (crop to the alpha bounding box).
    A generated illustration usually fills only the middle ~50% of its frame; if you do
    not crop, the visible art sits far inside its box and reads as mis-placed, and sizing
    is guesswork.
  - Do NOT "center the art in the gap between the text and the card edge". The text block
    has a ragged right boundary (the longest line sticks out, the shorter lines do not),
    so a geometric center between text-right and card-edge looks off, the eye sees the
    larger whitespace beside the short lines. Instead frame SYMMETRICALLY: make the art's
    right margin to the card edge EQUAL the text block's left margin (the card padding,
    e.g. 46px). Text hugs the left inset, art hugs the right inset, the card frames
    evenly. Verify by the VISIBLE pixels, not the element box: the `<img>`
    `getBoundingClientRect` can include transparent inset (a stray crop pad or the art
    not reaching its own frame edge), so screenshot and scan the bright-pixel extent of
    the art and compare that right margin to the text's left margin. Crop tight (no
    padding) so the box equals the art. (In one case the element box implied a 16px gap
    while the visible art was actually 70px off the edge, it read as left-shifted.)

### 5.4 Style and line weight (consistency is everything)

One style string for the whole deck. Required traits:

- Editorial scientific line illustration, clean flat vector, confident and simple.
- **Uniform medium stroke weight** (about 3 to 4 px at 1024 px), rounded line caps,
  consistent across the whole image. Not hairline thin (reads as weak and low contrast),
  not heavy or bold. Use at most a couple of weights.
- Dark teal ink lines with selective cyan `#0e9bb5` and magenta `#c026a6` accents, with
  enough color that it also reads on a dark surface.
- A single balanced centered composition that fills its frame with a comfortable margin,
  not a tiny motif in a corner, limited detail, generous internal spacing.
- Absolutely no text, words, letters, numbers, labels, or logos in the image.

### 5.5 Variety: unique per slide, never a reused motif

Generate a distinct illustration for each illustrated slide, with the concept derived
from that slide's own title and first bullet or body line. Do NOT build a small motif
library and map it by keyword: it collapses (in one real run, a single "guardrail" motif
matched 17 of 22 slides and the deck looked monotonous). Heroes for dividers are unique
too. The shared style string keeps them coherent; the per slide concept keeps them
varied.

---

## 6. Diagrams and SVG (the tiny text trap)

When you render a diagram as an SVG with a fixed `viewBox` that then scales down to fit
the slide, text sized in viewBox units shrinks with it. So **size SVG text generously
in viewBox units** or it becomes unreadable in a big cell.

Concrete, tested values (viewBox roughly `980 x 470`):

- matrix 2x2: quadrant title `25`, weight 800; item text `19`; axis labels `17`. Pad
  cells `24`. Allow items up to 3 wrapped lines so they do not truncate.
- pipeline: boxes HUG their content (compute box height from the text, do not use a
  fixed tall box) and the text is VERTICALLY CENTRED inside, so there is never a big
  empty box with tiny text floating at the top. WRAP to two rows (snake layout: row one
  left to right, a down arrow, row two right to left) when there are more than about 5
  steps, so the boxes stay wide and the text stays large. Step title `20–24`, step desc
  `15–17`, arrows `22–24`. A single row of 7 narrow boxes is too small for a hall.
- bars: label `17`, value `16`.
- timeline: keep node text terse (about 80 characters), 4 lines max; long descriptions
  truncate. Shorten the content, do not shrink the font.

General rule: if a diagram cell is more than about 40% empty, the text is too small or
the cell is too big. Grow the text or shrink the cell.

---

## 7. The generation pipeline (scripts)

Keep four small scripts in a `_review/` folder. They are reusable across decks.

- **`transparent.py`** key white to transparent (section 5.2).
- **`artify.py`** for each slide: derive a concept, generate on white with the shared
  style (skip if the file exists, so it is idempotent and resumable), key to
  transparent, and write the `hero` (dividers) or `spot` (content) path into the deck
  JSON. Unique per slide (section 5.5).
- **`shotdeck.mjs`** Playwright screenshots: capture each slide's `.stage` at a 2x
  device scale, and the web index as a full page. Usage:
  `node shotdeck.mjs <file.html> <prefix> <all|1,2,3|page>`.
- **`grade.py`** run the vision grader (section 9) over the screenshots and print a
  score table plus a JSON of the worst slides.

The build step reads the deck JSON and writes self contained HTML (CSS and JS inlined),
one file per deck, plus the index and any hidden study dossier. Static, no local build
server needed; deploy by pushing (for example Vercel builds on push).

---

## 8. Illustration generation prompt template

```
<PER-SLIDE CONCEPT: "a unique, specific editorial illustration that represents:
 '<slide title>'. Focus on: <first bullet or body line>. Wider context: <one line
 about the deck's domain>. Make it visually distinct.">
+
<SHARED STYLE STRING from 5.4, ending with the hard 'no text' constraint>
```

Generate, then key to transparent, then place via the split grid or corner rule.

---

## 9. Verification loop: Playwright + Gemini vision, iterate until it passes

You do not get to call a deck done by looking at the JSON. Render it, screenshot every
slide, and have a vision model grade each one. Fix, rebuild, re grade. Repeat.

### 9.1 Vision grader

Use the current fast Gemini vision model (the project used `gemini-3.5-flash`; verify
the latest fast multimodal id each run, same rule as 5.1). Send one slide image with a
strict critic prompt and `responseMimeType: application/json`. Ask for:

```json
{
 "score": 1-10,
 "overflow": true/false,        // text clipped, cut by an edge, or running off the stage
 "has_visual": true/false,
 "issues": ["overflow","clipping","too-many-bullets","crowding","empty-space",
            "misalignment","low-contrast","tiny-text"],
 "diagram_suggestion": "if bullet heavy, name the better layout (flow/timeline/matrix/kpi/bars) or empty",
 "verdict": "one sentence"
}
```

Critic prompt must hard fail (score <= 5) on any text clipped or cut by an edge, and must
reward a clean headline plus 3 to 5 short bullets (7 to 8). Tell it the exact style so it
judges against the intended look, not a generic template.

### 9.2 How to act on grades

- **`overflow: true`** is the only must fix every time. But verify it by eye: this critic
  runs at temperature and produces false positives on sparse minimalist slides and on
  intentional edge bleed art (it calls them "clipping"). Open the screenshot. If it is
  genuinely clipped, fix it; if not, ignore and note the false positive.
- **`tiny-text`** on body copy: bump the size (often an SVG diagram, see section 6).
- **`too-many-bullets` / `crowding`**: cut content or split the slide.
- **`empty-space`**: this critic is biased against whitespace and will flag clean
  minimalist slides at 6 to 7. Do not chase it into clutter. Fix it only when the slide
  genuinely has a stranded tiny element (then enlarge the visual or rebalance the grid),
  not when the whitespace is intentional framing.
- **`diagram_suggestion`**: if a bullet slide would be clearer as a diagram, convert it.

### 9.3 Loop and stop condition

Screenshot all, grade all, fix the real issues, rebuild, re grade the changed slides.
Stop when: zero genuine overflow, no `tiny-text` on body copy, no slide below 6 after
eyeball confirmation. Expect a minimalist deck to average about 7; that is good, the
critic caps whitespace heavy slides there. Record what you skipped as a false positive so
the next pass does not re chase it. Never silently accept a real overflow.

### 9.4 Mobile and dark surfaces

Also screenshot the web index full page (it has a dark header) and at a phone width.
Confirm: header art does not box over the title, transparent art still reads on the dark
gradient, and the deck is legible at small size.

---

## 10. Typography, color, contrast checklist

- One gradient accent per headline, on one or two words only. Never gradient a whole
  paragraph.
- Headline line wrapping: set `text-wrap:balance` on every headline (h1, h2, h3,
  statement, quote) and give titles a generous `max-width` (about 36 to 40ch for a slide
  h2), NOT a tight one. A tight `max-width` plus no balancing produces ugly orphans (a
  short title broken so that one word sits alone on the second line). With balance, a
  short title stays on one line and a long title splits into two roughly equal lines. An
  orphan single word on its own line is a fail.
- Body text `--ink-2` (about `#33425a`), secondary `--ink-3` (about `#5d6c82`). Do not go
  lighter than `--ink-3` for anything a reader must read.
- Kickers, footers, labels, code, and numbers in mono. Leads and quotes in serif.
  Headlines and UI in the display face.
- Minimum on screen body size about `1.9cqw` (roughly 24px at full size), and never
  below 20px for anything the audience reads. Captions, footers, and page numbers may be
  smaller but never carry primary content. Verify on a real projector mindset: if you
  would squint from 8 meters, it is too small.
- **No orphan line breaks.** Never let a short headline or line wrap so that one or two
  words drop to the next line; a ragged orphan looks broken on a big screen. If the text
  is short, keep it on one line: tighten the words, widen the box's `max-width`, or use a
  non-breaking space between the last two words. Only allow a wrap when the line is
  genuinely long, and even then break it where it reads naturally, not into a stray word.
  Cells and text blocks always keep their padding and gaps so they breathe; do not crush
  content to an edge to avoid a wrap, fix the content instead.
- **Widows and orphans (Czech typography).** Never leave a single-letter preposition
  (`k s v z o u`) or conjunction (`a i`) at the END of a line, and never strand an opening
  bracket plus preposition (`(v` at a line end is wrong). Tie them to the next word with a
  non-breaking space (`&nbsp;` / U+00A0), e.g. `v&nbsp;provozu`, `(v&nbsp;produkci`, and a
  number to its unit (`20&nbsp;%`). The non-breaking space is the right fix, not a manual
  `<br>` (which breaks at the wrong place when the box width changes).

---

## 11. Content and integrity rules

- No em dash characters anywhere a person reads (slides, index, this file). Use colon,
  comma, parentheses, or restructure. En dash only for numeric ranges.
- One idea per slide; the face is short, the speaker notes carry the argument. Every
  slide should have 4 to 8 sentence notes with the point and a citation.
- Truth in materials: describe only what is built; label proposals as proposals; cite
  external systems with a year. If any content is forward looking, the web index must
  show a visible disclaimer strip. Mark mockups in the file name.
- `noindex, nofollow` on semi public decks; password gate if needed.

---

## 12. Pre ship checklist

1. Every slide: one idea, headline reads in 2 seconds, only core ideas on the face.
2. Projector legible: body text >= 24px equivalent, no slide auto scaled below ~0.9. All
   the detail you removed from faces lives in the speaker notes (nothing lost). Split any
   slide that cannot be both readable and complete.
4. No overflow (vision verified and eyeball confirmed), no text under an illustration.
5. Illustrations: unique per slide, uniform medium line weight, transparent, placed in a
   grid column or corner with breathing room; light slides only, dark dividers clean.
6. Diagrams: text large enough to read, cells not mostly empty.
7. Two col slides: even card count, or odd count with the last card centered on its row
   (never a dead quadrant).
8. Type scale and color tokens consistent across all slides; no orphan line breaks (no
   one or two words wrapping alone); cells keep padding and gaps so they breathe.
9. Web index: header art clear of the title; disclaimer if anything is aspirational.
10. Mobile and dark header checked.
11. No em dashes. Citations present. Notes present.
12. Vision grade pass recorded; deck deployed; live URL checked (HTTP 200, images load).

---

## 13. Reference scripts

Minimal, reusable versions of the four scripts live alongside this file
(`scripts/transparent.py`, `scripts/artify.py`, `scripts/shotdeck.mjs`,
`scripts/grade.py`). They are copied from the working `34_shape_agent/_review/` set.
Adapt the model ids per section 5.1 before each run.

## 14. Model version table (verify before every project)

| role            | current id (June 2026)        | nickname        | note |
|-----------------|-------------------------------|-----------------|------|
| image, quality  | `gemini-3-pro-image-preview`  | Nano Banana Pro | heroes, key art |
| image, fast     | `gemini-3.1-flash-image`      | Nano Banana 2   | bulk spot art |
| vision critic   | `gemini-3.5-flash` (verify)   | Gemini Flash    | grading loop |

Always web search to confirm these are still current at the start of a project, and
update the scripts. If a better model exists (Google or another vendor), use it and note
the change.

---

Sources that informed this manual: the `21_ai_academia` deck (container query type
scale, grid based illustration columns, component library), BrightCarbon and Design Shack
2025 on intentional whitespace and visuals that carry weight, IBM Design Language and
Princeton University Press on consistent line weight, and Google AI / DeepMind docs on
the Gemini 3 image models (Nano Banana Pro / 2).
