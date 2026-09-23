# Template-native deck-generation system

Deterministic system that turns a JSON spec of *intents* + *content* into a
branded PowerPoint deck. Built incrementally over phases 1–14 around the
Oliver Wyman template (Marsh Serif heading / Noto Sans body, the OW navy
palette, the warm-cream `F7F3EE` default fill, and the amber `FFBF00`
accent).

## v3.5 — Multi-level org charts

The `show_org_chart` intent now supports arbitrary tree depth. Previously
it was hardcoded to two levels (root + flat row of direct reports); now
it accepts a recursive `children` list on every node and lays out
4–5+ level hierarchies correctly.

  - **Recursive node shape** — every node accepts ``children``:
    ```json
    {
      "name": "Anna Müller", "title": "CEO",
      "children": [
        {"name": "Lukas Weber", "title": "CFO",
         "children": [{"name": "Marie Klein", "title": "Treasury", ...}]},
        ...
      ]
    }
    ```
    The legacy ``{"root": {...}, "reports": [...]}`` shape still works —
    if the root has no ``children``, the runtime promotes ``reports`` to
    ``root.children`` automatically.

  - **Leaves-proportional placement** (Reingold–Tilford style) — each
    subtree gets a horizontal slot proportional to its leaf count, then
    nodes center within their slot. Wide branches get more space than
    narrow ones; everything packs tight without overlaps.

  - **Bus-line connectors** — parent drops to a horizontal bus halfway
    between levels, the bus spans all children, each child rises from
    its top-center. Single-child parents skip the bus and use a
    straight drop. Same orthogonal look readers expect from an org chart.

  - **Adaptive sizing** — box width and height plus name/title font
    sizes scale with tree depth and breadth so 5-level / 21-node trees
    still fit the standard content area without the layout going off the
    slide. Three font tiers (12 → 10 → 8pt, all design tokens) keyed
    on the resulting box geometry.

## v3.4 — Composition grids (text + chart per cell)

The card-grid mechanism from v3.3 generalizes: each cell can now host a
stacked composition of text + native chart (and the grid shape is
author-controllable). Same intent (`dashboard`), same JSON, just optional
new fields.

  - **`chart` per metric** — adding a `chart: {...}` to any metric routes
    that cell through the *composition* renderer: label/value/delta in
    the upper ~1.2", a column-width native chart filling the remainder.
    The chart inherits all the v3.2 OW styling (palette, axes,
    gridlines), then has its legend, data labels, and value-axis ticks
    suppressed because there's no room for them at cell scale.

  - **`grid` override** — adding `grid: "2x3"` to the content forces an
    explicit grid shape regardless of item count. Convention is
    **rows × cols** (matrix/numpy). So `"1x4"` is a horizontal strip of 4,
    `"2x3"` is a wide 2-row × 3-col grid, `"3x2"` is a tall 3-row × 2-col
    layout. Tuples `(rows, cols)` are also accepted (face-value, no
    reversal).

  - **Unified routing** — `_split_for_variadic_overflow` now triggers the
    grid path when *any* of three signals fire: explicit `grid` set, any
    cell carries a `chart`, or the classic variadic overflow. The first
    signal that matches wins; the routing decision is logged inline.

  - **Refactor** — `draw_card_grid` is now a dispatcher onto
    `_draw_kpi_cell` (text-only, v3.3 behavior), `_draw_composition_cell`
    (text + chart), and `_draw_chart_only_cell` (chart with no header).
    Per-cell geometry decisions live in one place.

## v3.3 — Card-grid overflow

KPI dashboards with more metrics than any layout's slot count (e.g. 8 metrics
on a 4-column layout) used to paginate across multiple `(continued)` slides.
The OW preference (per the `8_cards.pptx` reference, slide 3) is to draw all
cards on a single `Title Only` slide as a synthetic grid. v3.3 implements
that path.

  - **`runtime.draw_card_grid()`** — given a list of items, picks a grid
    size and draws each card as a real `MSO_SHAPE.RECTANGLE` with the same
    fill, insets, and typography as `fill_kpi`. Because shapes don't
    inherit master typography, every paragraph is set explicitly via the
    existing `apply_text_level()` helper (level 5 for label/delta, level 6
    for value), then sizes are overridden run-side (11pt label, 34pt value).
    Grid sizes scale with item count: 1×n for n≤4, 2×3 for 5–6, 2×4 for
    7–8, 3×4 for 9–12, capped at 4×4 beyond that.

  - **Compiler intercept** — `_split_for_variadic_overflow` now branches on
    the variadic slot's strategy. If it's `kpi_card` and the list overflows,
    emit a single canvas-targeted plan with the new `kpi_card_grid` strategy
    on `Title Only`. Other variadic intents (long bullet lists, long tables)
    keep the old per-page chunking, since pagination is the right answer
    for prose. The split path remains as fallback for templates whose
    `Title Only` layout can't host free shapes (rare).

  - **`kpi_card_grid` strategy** — registered in `STRATEGIES`; takes the
    full metrics list as payload and forwards to `draw_card_grid`. Same
    shape as the canvas strategies used for org charts, pyramids, and
    process chevrons.

The pattern generalizes: any future "card-like" content type that doesn't
fit the placeholder model can plug into the same overflow branch by adding
its own canvas-grid strategy. The integration point is one block in
`_split_for_variadic_overflow`.

## v3.2 — Chart styling

Charts now render to the OW spec extracted from the official chart templates
(`Bar.crtx`, `Column.crtx`, `Column_Stacked.crtx`, `Doughnut.crtx`,
`Line.crtx`) and the `Chart_Templates` reference deck. The complete
implementation is in `runtime.py::_theme_chart` plus its helpers.

  - **15-color series palette** — six theme accents (navy, sky blue, light
    blue, warm grey, light grey, greige) followed by nine explicit overrides
    (`#CB7E03`, `#FFBF00`, `#FFD98A` orange/yellow family; `#2F7500`,
    `#6ABF30`, `#B0DC92` green family; `#8F20DE`, `#DEB1FF`, `#F5E8FF`
    purple family). Defined in `OW_CHART_PALETTE`.
  - **Axes** — category axis has a thin `tx1` line and no gridlines; value
    axis has `<a:noFill/>` (invisible) and major horizontal gridlines in
    `#D1CEC9` at 0.75pt. Tick marks suppressed on both. Tick labels at 12pt
    minor font, weight normal.
  - **Data labels** — value-only, 12pt minor font. Position is per chart
    type: `outEnd` for clustered column/bar, `ctr` for stacked and pie/
    doughnut. Stacked charts get auto-contrast label colors (white on dark
    series, dark on light) computed from sRGB luminance.
  - **Legend** — bottom, no overlay, 12pt minor font. Suppressed entirely
    for single-series charts.
  - **Bar/column geometry** — `gapWidth` and `overlap` set per (barDir,
    grouping) to match the reference: column clustered 220/-50, column
    stacked 219/100, bar clustered 200/-25.
  - **Line charts** — 2.25pt stroke (28 575 EMU), markers off for plain
    `line`, cycled marker shapes for `line_with_markers`.
  - **Doughnut** — `holeSize=75` (thin ring per OW spec).
  - **Auto-title suppression** — `<c:autoTitleDeleted val="1"/>` on every
    chart so single-series charts don't surface the series name above the
    plot.

## v3.1 — Filled-callout style update

Filled callout placeholders (the "insight" panel beside chart_insight slides
and the cards on dashboard slides) now match the OW reference:

  - **Cream fill** (`F7F3EE` via `BRAND_COLORS["default_fill"]`) instead of
    navy. Dark text reads naturally; no more white-on-navy contrast tricks.
  - **No border** — the line is set to `<a:noFill/>`. The card reads as
    a panel, not a framed box.
  - **Explicit 0.2" insets** on all four sides via `<a:bodyPr lIns/.../>`.
    Without this, PowerPoint inherits ~0.1" from the master and the text
    crashes into the chart's legend on the adjacent placeholder.
  - **Level inheritance for typography.** The eyebrow label uses level 5
    (Subheading: 12pt minor, not bold) shrunk to 11pt. The body line uses
    level 6 (Small primary: 26pt major Latin, not bold) — size and font
    come from the master via `paragraph.level = 6`, no run-level overrides.
    This delivers the "strong short statement in the primary font" treatment
    the brand spec calls for, while remaining compliant with
    `BRAND_RULES["primary_font_never_bold"]`.

The change is local to three methods on `TemplateRuntime` (`_style_card`,
`fill_kpi`, `fill_insight`) plus one new helper (`_set_body_insets`). The
public API is unchanged; existing JSON keeps working without edits.

## Quickstart

```bash
pip install -r requirements.txt

# Build one of the shipped example decks (slides that exceed layout
# capacity split automatically, so output can have more slides than the spec)
python src/generate_deck.py \
    --template ow_default.pptx \
    --deck examples/semantic_deck.json \
    --output semantic.pptx
```

## What's in this package

```
.
├── ow_default.pptx        ← the OW-branded template (18 layouts)
├── requirements.txt
├── src/                   ← runtime.py (rendering/OOXML) · compiler.py (intents,
│                            layout scoring, strategies) · generate_deck.py (CLI)
│                            · gate.py · icons.py · autolayout, cards, voice, design modules
├── examples/              ← visuals_deck.json (every visual primitive) ·
│                            semantic_deck.json (overflow-split paths)
└── tests/                 ← pytest suite (smoke + invariants + parity)
```

## Architecture in three layers

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  generate_deck   │ →  │     compiler     │ →  │     runtime      │
│   (CLI / I/O)    │    │   (semantic →    │    │  (rendering /    │
│                  │    │    plan)         │    │   OOXML)         │
└──────────────────┘    └──────────────────┘    └──────────────────┘
                              ↓                         ↓
                        ┌──────────────────┐    ┌──────────────────┐
                        │   intents +      │    │   draw methods   │
                        │   strategies     │    │   (chevrons,     │
                        │                  │    │    pyramid, …)   │
                        └──────────────────┘    └──────────────────┘
```

**`runtime.py`** — knows the OW template, the theme, and OOXML.
- Loads the theme palette and master font references from the template.
- Provides primitives: `set_title`, `fill_bullets`, `fill_plain_text`,
  `fill_kpi`, `add_chart_native`, `bind_table_to_placeholder`,
  `add_conclusion`, `add_footnote`, plus engine compositions
  (`draw_process_chevrons`, `draw_pyramid`, `draw_cycle`, `draw_org_chart`).
- Owns the brand spec: `BRAND_RULES`, `BRAND_COLORS`, `BULLET_LEVELS`.
- Owns the per-slide content-area override mechanism so canvas strategies
  re-fit when bottom adornments are present.

**`compiler.py`** — turns a slide spec into one or more execution plans.
- The intent registry maps intent names like `show_data`, `dashboard`,
  `show_process` to slot definitions.
- Layout scoring picks the best layout per intent.
- Strategies dispatch to runtime primitives.
- The split paths handle overflow:
  - **Variadic** — list slot longer than layout's slot count → chunk across pages
  - **Density** — bullet count or table size exceeds slot capacity → split content

**`generate_deck.py`** — `argparse` wrapper. Reads the deck JSON, calls
`compile_slide` on each slide, executes each plan via the runtime, saves.

## Slide-spec syntax

Every slide is a single JSON object:

```json
{
  "intent": "<intent name>",
  "content": { ...intent-specific... },
  "conclusion": "Optional one-line takeaway",
  "footnote":   "Optional source / disclaimer"
}
```

`conclusion` and `footnote` are slide-level adornments — they work on any
intent, on any layout. Both are optional. When present, the system reduces
the content area so canvas-rendered content (chevrons, pyramid, etc.)
doesn't overlap them.

### Available intents

This table is the **canonical content-schema reference** — the single source of
truth for the `content` keys each intent takes. Other docs (e.g.
`16_deck_spec_authoring.md`) point here rather than restating it; the full intent
registry with support levels is `20_slide_design_capability_map.md`.

| Intent | Content keys | Notes |
|---|---|---|
| `introduce_topic` | `title`, `subtitle`, `image?` | Title slide (cover image optional) |
| `section_divider` | `title`, `number` | Section break with big number |
| `explain` | `title`, `body: {heading, bullets}` | Bullets may nest: an item can be `{text, bullets:[...]}` for sub-bullets (to 3 levels: • / – / -). No fixed bullet cap — the engine splits across slides only when content overflows the area. |
| `show_data` | `title`, `table` *or* `chart` | Table overflows on >~10 rows |
| `compare_two_options` | `title`, `left: {heading, bullets}`, `right: {heading, bullets}` | Two-column option/trade-off comparison |
| `dashboard` | `title`, `metrics: [{label, value, delta}]` | Variadic-overflows on >4 metrics |
| `show_trend_with_key_message` | `title`, `chart`, `insight: {title, text}` | 2/3 chart, 1/3 insight callout |
| `show_waterfall` | `title?`, `waterfall: {orientation:'vertical'|'horizontal', categories[], values[], totals[], heading?, subheading?}` | Waterfall/bridge chart: absolute totals (indices in `totals`) drawn from zero in navy; deltas float on a transparent base — green up / red down (vertical) or light-blue (horizontal). Magnitude labels on bars. |
| `show_treemap` | `title?`, `treemap: {items:[{label, value}], heading?, subheading?}` | Treemap (squarified): rectangles sized by value, OW palette with white seams, labelled with name + value. Part-to-whole across many categories. |
| `show_process` | `title`, `steps: [{label, heading?, bullets?}]` | Chevron flow; "large" mode when no bullets |
| `show_pyramid` | `title`, `levels: [{label}]` | Top-down stacked trapezoids |
| `show_cycle` | `title`, `items: [{label}]` | Ovals on a circle with arrows. Use only for genuine cycles/loops, not to list parallel topics. |
| `show_org_chart` | `title`, `org_chart: {root, reports}` | 2-level org chart |
| `show_quote` | `title?`, `quote: {text, attribution}` where `attribution` is a string *or* `{name, title, location}` | Large left-aligned Marsh Serif statement quote in Text 1; Name/Title/Location attribution below; no rule line. The OW source design has a headshot on the right (no image pipeline — rendered text-only). |
| `show_graphic_with_text` | `title`, `panel: {graphic: {kind, ...}, text: {heading, subheading, bullets\|paragraphs}, side: "graphic_left"\|"graphic_right"}` | Composite: a graphic in one pane, supporting text in the other. `graphic.kind` ∈ growing_steps, pyramid, cycle, org_chart, process, matrix, timeline (data under the kind's usual key). `side` puts the graphic left (supported by text) or right (supporting text on the left). |
| `introduce_person` | `name`, `role`, `photo`, `bio: {heading, bullets}` | Bio with photo |
| `summary` | `title`, `body: {heading, bullets}` | Closing takeaways |

### Chart types (for `show_data` and `show_trend_with_key_message`)

`column_clustered`, `column_stacked`, `column_stacked_100`,
`bar_clustered`, `bar_stacked`, `line`, `line_with_markers`, `pie`,
`doughnut`, `area_stacked`, `xy_scatter`. Specified as the chart's `type`
key.

## Brand spec (Phase 14)

Three things, codified in `runtime.py`:

```python
BRAND_RULES = {
    # The "primary"/major Latin font (Marsh Serif). NEVER bold.
    "primary_font_never_bold": True,
}

BRAND_COLORS = {
    "default_fill":      "F7F3EE",   # warm cream — every decorative shape
    "subtle_highlight":  "accent3",  # CEECFF
    "strong_highlight":  "accent1",  # 000F47 navy
    "text_highlight":    "FFBF00",   # amber, same as Conclusion's left rule
}

BULLET_LEVELS: Dict[int, TextLevel] = {
    0: ("Body",          12, "minor", False, None, 0,     0      ),
    1: ("Bullet 1",      12, "minor", False, "•", 0.197, -0.197 ),
    2: ("Bullet 2",      12, "minor", False, "–", 0.394, -0.197 ),
    3: ("Bullet 3",      12, "minor", False, "-", 0.591, -0.197 ),
    4: ("Heading",       12, "minor", True,  None, 0,     0      ),  # the only bold level
    5: ("Subheading",    12, "minor", False, None, 0,     0      ),
    6: ("Small primary", 26, "major", False, None, 0,     0      ),
    7: ("Medium primary",40, "major", False, None, 0,     0      ),
    8: ("Large primary", 54, "major", False, None, 0,     0      ),
}
```

Levels 0–8 were extracted directly from the OW master's `<p:bodyStyle>`.
Strategies that put text in placeholders set the paragraph level and let
the master cascade. Strategies that put text in free text boxes call
`apply_text_level()`, which applies the values explicitly *and* enforces
`primary_font_never_bold` regardless of what the level table says.

## Compiler invariants (the contract)

These hold across every code path:

1. Intents are *data*, not behavior — the compiler doesn't touch OOXML.
2. The capability filter is a hard gate: a layout can only render an
   intent if the layout exposes the slots the intent demands.
3. `compile_slide` returns a `List[CompilationPlan]` — possibly multiple
   plans for one source slide when overflow splits trigger.
4. Variadic splits chunk; density splits split content; nothing is ever
   silently truncated.
5. Layout scoring is deterministic — same inputs always pick the same
   layout.
6. Strategies are pure dispatchers: they take `(runtime, slide,
   placeholder, payload)` and call runtime primitives. No OOXML in
   strategies.
7. Canvas-targeted instructions don't gate slot-count compatibility.
8. `PICTURE` placeholder mutation uses native `insert_picture`; charts
   and tables use lxml `<p:ph>` transfer.
9. `Conclusion` and `Footnote` propagate to every plan in a split — when
   a slide overflows, both adornments appear on each split.
10. Decorative shape fills default to `BRAND_COLORS["default_fill"]`
    unless a strategy explicitly chooses `subtle_highlight` or
    `strong_highlight` for a semantic reason.
11. `apply_text_level()` is the only sanctioned way to apply per-level
    styling to text outside a placeholder. Major-font runs cannot be
    bolded through it.

## Known limitations / future work

- **Conclusion height sizing is behind a flag.** `ADJUST_CONCLUSION_HEIGHT`
  (runtime.py) is currently `False`: the conclusion uses a fixed single-line
  height, so keep conclusions punchy (one line, ~85 chars). Flip the flag to
  restore line-count-aware upward growth from the pinned bottom edge.

- **Layout placeholder shrinking.** When a non-canvas layout has content
  placeholders extending below y=6.5, those aren't dynamically shrunk
  for the conclusion adornment. The OW layouts don't usually trigger
  this in practice, but it's not handled generically.

- **Chart styling is theme-default.** Series colors come from the OW
  theme's accent palette, not a curated chart-style spec. A `chart_styles`
  block in the brand spec (axis colors, gridline visibility, marker style
  per chart type) is a reasonable next addition.

- **No SmartArt.** The system uses engine-composed shapes (
  `MSO_SHAPE.CHEVRON`, `MSO_SHAPE.PENTAGON`, etc.) drawn directly. Real
  PowerPoint SmartArt would require generating five XML parts plus
  layout-algorithm references — a project-sized effort that was
  deliberately deferred.

## Editorial prose body

`explain` and `summary` bodies accept a `paragraphs` list (or `"format": "prose"` alongside `bullets`) to render report-style prose — flush-left paragraphs, no bullet glyphs, spaced — instead of a bulleted list. Used by the longform voice profile.

## New visual intents (any size)

- **`show_matrix`** — N×M matrix across two axes. Content key `matrix`:
  `{"rows": 3, "cols": 3, "x_axis": "Effort", "y_axis": "Impact",
  "highlight_cell": [row, col], "items": [{"label": "...", "x": 0.8, "y": 0.7,
  "comment": "..."}]}`. `x`/`y` are 0–1 (0 = left/bottom). Items unlimited;
  `rows`/`cols` arbitrary (2×2, 3×3, 5×5, …). `highlight_cell` and per-item
  `comment` are optional; items may use `{"row": r, "col": c}` instead of x/y.
- **`show_timeline`** — horizontal timeline. Content key `milestones`:
  `[{"date": "Q1", "title": "Kickoff", "description": "..."}]`. Any number;
  milestones alternate above/below the axis and fonts scale with count.
- **`show_growing_steps`** — ascending staircase. Content key `steps`:
  `[{"label": "Pilot", "description": "..."}]`. Any number; the final step is
  rendered as the highlighted target state.

All three render on the Title Only canvas and accept `conclusion`/`footnote`.

- **`show_columns`** — 2-5 parallel headed text columns. 2-4 use the template's native column layouts (master-styled placeholders); 5 falls back to a manual canvas layout. No vertical rules.
  Content key `columns`: `[{"heading":"Strengths","bullets":[...]}]` (each
  column may use `bullets`, `paragraphs`, or `text`). Use for parallel
  categories instead of a single flat bulleted body.

- **`show_contents`** — table of contents on the native Contents layout.
  Content key `sections`: `[{"title": "Market context", "page": 4}]`. Any
  number; numbers auto-fill as 01, 02, … (set `number` to override, or `""`
  for an unnumbered entry like an Appendix); `page` is optional. The title
  defaults to whatever you pass (use "Contents"). No conclusion/footnote
  (the Contents layout is adornment-free by rule).
| `compose` | `title?`, `compose: {rows:[{height?, regions:[{block, data, width?}]}]}` or `{regions:[...]}` | Open composition (escape hatch): heterogeneous blocks — chart/text/waterfall/treemap/diagram — on a grid of regions. Use only when no preset fits; the fit router prefers a named preset when one matches. |

### Composer block kinds
A `compose` region's `block` is one of: `text` (heading + bullets/paragraphs), `kpi` (heading + stacked {value,label,delta}), `table` ({headers, rows}), `image` (captioned placeholder panels — no image pipeline), `chart` ({chart:{type,...}}, any type: column/bar/line/pie/doughnut/area/scatter), `waterfall`, `treemap`, or any diagram (`cycle`/`pyramid`/`process`/`org_chart`/`matrix`/`timeline`/`growing_steps`). Each renders into its region via the unified block dispatcher.

### Auto routing (router always in the loop)
Set `deck.audience` (e.g. `board`, `executive`, `client`, `internal`, `project_team`) on the deck. Emit a content slide as `{"intent":"auto","content":{"title":..., "regions":[{block, data}, ...]}}` and the compiler routes it through `route_composition`: if the region set matches a preset at fit ≥ the audience threshold it snaps to that preset's canonical proportions, otherwise it composes freely. The decision is logged in the build output. Named intents and explicit `compose` still work as before; `auto` is the path that always consults the threshold.

### Native treemap
`show_treemap` and a `chart` block with `type: "treemap"` now emit a NATIVE PowerPoint treemap (a `cx` chartEx object), not drawn rectangles. Schema unchanged: `{treemap:{items:[{label,value}]}}` or a chart with `categories`+`series`. Set `treemap.render: "drawn"` to force the portable squarified version instead (e.g. for non-PowerPoint viewers). Native treemaps render in PowerPoint; headless/non-PowerPoint previews cannot draw chartEx, so they show blank there.

### Quote and contents layouts
`show_quote` renders one textbox (width 10"): the quote in Marsh Serif 54pt with 12pt space-after, then Name / Title / Location in Noto Sans, all left-aligned with a 0.25" left + hanging indent in the SAME textbox. `show_contents` is a native border-less 3-column table — section number (auto 01,02,…; set `number:""` to omit) | section name | page — all rows top-aligned at 16pt on the Contents layout (one per deck).

---

## Icons & images authoring (v3.6)

**Icons.** Add an `icon` (optional `icon_color`, default navy `000F47`) to items of:
- `show_columns` → each `columns[]` item
- `dashboard` → each `metrics[]` item

The icon renders at the top of the slot and the text is pushed below it. Values
are concept names from the curated ~500-icon set — see `23_icon_index.md` for the
full categorised list of names to use (e.g. `chart`, `growth`, `users`, `target`,
`shield`, `cloud`, `leaf`, `briefcase`). Heroicons-style names (`chart-bar`,
`light-bulb`, `device-phone-mobile`, `user-group`, …) and close synonyms also
resolve via the runtime's alias map, so a natural guess still lands. Icons are
native editable freeforms (navy / Text 1), not images. Never put icons on
cover/structural/legal layouts.

```json
{"intent": "show_columns", "content": {"title": "Pillars", "columns": [
  {"heading": "Growth", "icon": "arrow-trending-up", "bullets": ["New segments"]}]}}
```

**Images.** Image-bearing slots accept: `path` (file), `source` (a deck-level id
for reuse), `prompt` (generation, only if enabled), `label` (person monogram
fallback), plus `aspect` ("16:9"/"1:1"/"21:9"…) or explicit `crop`
{left,top,right,bottom}, and `name` (→ shape `REPLACE:<name>` for designer swap).

- `introduce_topic.image` — optional cover image (uses the *Title Slide with Picture* layout; omit for a plain cover).
- `introduce_person.photo` — bio headshot.
- `compose` `image` blocks — `{"block":"image","data":{"source":"hero","aspect":"1:1","name":"…"}}`.
- **Reuse one photo across slides with different crops** via a deck-level map:

```json
{"images": {"hero": {"path": "hero.jpg"}},
 "allow_image_generation": false,
 "slides": [ /* …use {"source":"hero","aspect":"16:9"} and {"source":"hero","aspect":"1:1"}… */ ]}
```

Rules: default to **swappable placeholders** — if an image slot has no usable
asset, a labelled swap-target panel is drawn (never silently empty), and
`introduce_person` with no photo falls back to a name monogram. Images are
**decorative/atmospheric only — never used to carry data or claims**.
`allow_image_generation` is `false` by default; turn it on only to fill
placeholders with generated imagery, treating output as replaceable. After save,
`generate_deck.py` runs the BoundHeight-style overflow check and reports any
shape whose text exceeds its box.

## Build gate — `gate_result.json` (machine-readable, non-overridable)

`generate_deck.py` writes `gate_result.json` next to the output after every
build. `passed` is a Python boolean — the model cannot declare success by
self-assessment; it must read this file.

HARD checks (any failure → `passed:false`, do not deliver):
- `overflow` — no fixed-box text exceeds its box (BoundHeight measurement)
- `icon_coverage` — item icons are all-or-nothing; warns on a lopsided mix (icons on some `show_columns` columns / `dashboard` KPIs but not all). All or none renders; a mix renders none.
- `action_titles` — content-slide titles are insight sentences, not topic labels

WARN checks (never block, but surface to the user):
- `image_slots` — count of `REPLACE:` placeholders still to fill
- `sources` — content slides cite a `source`/`footnote`

Shape: `{ "passed": bool, "overall_score": int, "verdict": str,
"fail_items": [...], "warn_items": [...], "checks": {...} }`. On `passed:false`,
fix every `fail_items` entry and rebuild until `passed:true`.

### Composite components (canvas intents)
- `stat_callout` — big-number stat cards: `{title, stats:[{value, heading, text}]}` (1-4), cream cards.
- `icon_rows` — stacked fine-line icon + heading + text rows: `{title, rows:[{icon, heading, text}]}` (1-5).
- `compare` — two-column check/cross: `{title, compare:{pros:[...], cons:[...], pros_heading?, cons_heading?}}`.

- `sticker` — amber circular highlight + optional note: `{title, sticker:{text, note?}}`.

- `infographic` — native-freeform infographics: `{title, infographic:{type:funnel|gauge|venn, ...}}`. funnel `{stages:[{label,value}]}`, gauge `{value,label,suffix?}`, venn `{sets:[{label}]}`. Also usable as a `compose` block.

- `infographic type:heatmap` — native NxN cell grid + axis labels + stepped legend `{values:[[..]], x_labels?, y_labels?, steps?, legend_labels?, description?}`.

- All components are variadic (any number; stat cards wrap to a grid). Component text uses the design-system styles: **Heading 12pt bold, body 12pt, default navy**; icons sit 0.2" from the card top/left at 0.5" with text at a 0.9" top margin.
