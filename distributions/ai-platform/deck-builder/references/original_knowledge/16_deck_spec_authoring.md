# Authoring a deck directly (deck_spec)

The runtime is driven by one data structure — the **deck_spec** — and every input
mode produces it. This doc lets a precise brief skip the research interview and be
mapped (almost) literally to slides:

- **Direct-build in chat (mode b1):** the user describes slides ("a cover, then a
  comparison of A vs B, then a line chart with a takeaway"); map each description
  to an intent below and emit the deck_spec straight to `generate_deck.py`.
- **Authored file (mode b2):** the user hands you a `.json` **or** `.yaml` file in
  this shape. `generate_deck.py --deck file.yaml` loads it the same way as JSON.

Direct-build skips Phases 1–5 (no interview, research.json, or outline approval) —
the user has already done the thinking. Still run the **runtime gate** and never
deliver on a hard fail. If the brief is vague or makes factual claims you can't
verify, fall back to the normal interview instead of inventing content.

## Shape

```json
{ "slides": [ { "intent": "<name>", "content": { ... } }, ... ] }
```

One object per slide. `intent` picks the layout + renderer; `content` carries the
words and data. Unknown keys are dropped silently, so a typo fails quietly — check
the gate output.

**The `content` keys for every intent live in `01_readme_deck_system.md` →
"Available intents"** (the canonical schema — use those exact intent names, e.g.
`show_trend_with_key_message`, `show_quote`, `show_timeline`, not short forms).
The full registry with support levels is `20_slide_design_capability_map.md`.
This doc covers only what's specific to hand-authoring a deck_spec: the wrapper
shape (above), chart/table/compose syntax, adornments, and the voice×design
rules (below).

### Charts and tables

```yaml
chart:
  type: column_clustered   # or line, bar_clustered, pie, doughnut, area, ...
  categories: [Q1, Q2, Q3, Q4]
  series:
    - {name: Revenue, values: [100, 118, 132, 136]}
    - {name: Plan,    values: [100, 115, 130, 142]}
table:
  headers: [Region, FY24, FY25, YoY]
  rows:
    - [North, 4.1, 4.8, "+17%"]
    - [South, 3.2, 3.0, "-6%"]
```

Pick a **bar/column** chart to rank categories, a **line** for change over time;
avoid pie/doughnut beyond ~6 slices (the gate warns). Use a **table** for dense
numeric grids and **show_columns** (cards) for a few short text points — a small
text-only table is flagged by the gate.

On a **dashboard** with more than one chart, give each chart cell a `heading`
(and optional `subheading`) alongside its `chart` — the runtime renders them as a
Heading/Subheading text shape above the chart (not an embedded chart title), e.g.
`{heading: "Risk-adjusted ROI", subheading: "%", chart: {...}}`. A single-chart
slide needs no heading: its action title carries the message.

### Universal adornments (content slides only)

`conclusion` and `footnote` may sit at the **slide level** (beside `content`) or
**inside `content`** — both work; the compiler hoists a nested one. Bulleted text
always goes inside `body` (`body: {bullets: [...]}`), never as a bare `bullets` key.

- `conclusion`: one-sentence takeaway, rendered as the amber-ruled band.
- `footnote`: source line ("Source: …").
- `icon`: a one-word icon name on every `show_columns` column and `dashboard` KPI
  All-or-nothing: give every column/KPI an icon or none — a lopsided mix renders no icons (the runtime drops them all).
- Images **default to placeholders** (`REPLACE:<name>`) — a swap box with a
  paste-ready photoreal prompt — even on a direct build and even if the brief says
  "AI images". Use a real embedded `path` ONLY when the user explicitly asked to
  generate and embed real photos, and the file is a genuine photograph from your
  image tool saved to `/mnt/data`. **Never draw an image in code (PIL / matplotlib
  / gradients / shapes) and pass it as a photo via `path`** — if you can't make a
  real photo, use a placeholder and say so. See `02_runtime_bootstrap.md`.

Never put `conclusion`/`footnote` on covers, dividers, or legal layouts.

### Composition grid (N×M with spanning)

```yaml
compose:
  grid:
    cols: 3            # optional; omit to auto-pack
    rows: 2
    cells:
      - {block: chart, data: {type: line, categories: [...], series: [...]}, colspan: 2}
      - {block: text,  data: {heading: "Takeaway", bullets: ["...", "..."]}}
```

Equal tracks, fixed gutter; `colspan`/`rowspan` merge cells. A cell placed past the
declared `cols`/`rows` is a hard gate fail.

## Minimal YAML example

```yaml
slides:
  - intent: introduce_topic
    content: {title: Supplier consolidation review, subtitle: Procurement steering committee}
  - intent: explain
    content:
      title: Consolidating to two suppliers lowers cost and risk
      body:
        paragraphs:
          - Spend is split across nine suppliers today, none with real pricing power.
          - Two preferred suppliers would cover 80% of volume at better rates.
      conclusion: Consolidation cuts unit cost and concentrates accountability.
      footnote: "Source: FY25 procurement spend analysis."
```

Apply the house voice (`60_voice_system.md`), Standards, and Brand to the words even in
direct-build — the deck_spec controls structure, not style.

## Voice × design reconciliation (cards)

Where the house voice (`60_voice_system.md`) and the design rules meet on
cards, resolve as follows — these keep both intact:

- **Casing is a design transform, not author input.** The KPI/stat eyebrow renders
  in uppercase by design. Write the label in natural sentence case ("Cycle time",
  not "CYCLE TIME"); the engine applies the casing. The voice rule "sentence case
  for body / consistent capitalisation" does not forbid the eyebrow — the design
  owns that one visual transform.
- **Never ship a bare number.** The voice rule "interpret numbers; never just
  display them" governs how stat_card / kpi_card are used: always pair the `value`
  with an interpretive `heading` and/or `body`/`caption` that says what it means.
  The design provides the slots; the voice requires they carry meaning.
- **House voice applies to card text too.** The full house-voice rules
  (`60_voice_system.md`) — banned vague verbs, generic claims, number formats —
  apply to card headings, bodies and captions exactly as to any other text. The
  gate's banned-word and number checks read card text like any other run.
- **Functional colour is the sanctioned exception.** Green/red on the KPI trend
  glyph and traffic status come from the design system's existing `CHART_COLORS`
  (up/down) and signal status only — they are not decorative and do not widen the
  brand palette. All other card text stays navy or white.
