# Presentation Standards

Universal, mechanical standards for every OW deck — true regardless of audience,
voice, or intent. Applied at build (Phase 6) alongside Brand and the Design
System. This file owns *only* the universal mechanics. It does not set wording
(→ `60_voice_system.md`), flow/CTA (→ `13_intent_modes.md`), deck shape
(→ `14_content_structures.md`), or the argument (→ `15_storyline_logic.md`).

## Structure
- Structure first, slides second; let the intent flow drive the storyline
  (`13_intent_modes.md`, `15_storyline_logic.md`).
- One idea per slide. If a slide carries two ideas, split it.
- A title states a claim, not a bare topic label ("Margin fell 60bps on mix",
  not "Margin analysis"). The exact title *style* is set by the voice profile
  (`60_voice_system.md`): action-title for `consulting`, evocative-but-meaningful
  for `longform`.
- Open with the answer (or the question the deck resolves); close with a clear
  `summary` — conclusion, recommendation, or action.

## Content density
- Keep bullets to ≤ 2 lines each and let the compiler's overflow handling split
  content rather than cramming. There is no fixed bullet *count* — the per-slide
  bullet target is the voice profile's (`60_voice_system.md`); the engine splits
  across slides when content overflows, so grouping and depth are encouraged
  where they aid clarity.
- Nest sub-bullets (`{text, bullets:[...]}`, to 3 levels) where points have
  supporting detail, rather than keeping everything flat.
- Parallel items (2–5: strengths/weaknesses, pillars, workstreams, or a "when to
  use each" closer) → `show_columns` cards with an icon each — never a flat block
  of bullets *or* paragraphs. This applies especially to a closing/summary of
  parallel choices: cards show them side by side and fill the slide, where a
  paragraph list leaves it half-empty. Verbatim quotes → `show_quote`, never
  buried in a title.
- Don't cram a dense list into one narrow pane. If several items each carry
  multiple data points (e.g. 5 regions × investment/revenue/payback/rationale),
  give them room: use a two-column layout or a table across the full width, or
  split across slides — never let entries collide in a column too short for them.
  When a graphic shares the slide, keep the text side to the items that fit and
  move the rest to a second slide.
- Prefer one strong visual (chart/table/diagram) over decorative clutter; every
  element must support the slide's single message — cut the rest.
- Keep labels and body concise. The engine auto-fits and leaves genuine overflow
  for manual fix (sizes/floors in `50_design_system.md`) — concise content avoids
  shrinking; don't rely on it.

## Images on dense slides
- An image is optional adornment, not a required element. **Do not place an image
  on a slide that is already content-dense** — bullets + cards, a timeline + cards,
  a dashboard, or a chart + cards. Adding one squeezes the real content until it
  collides or overruns (the gate's overflow check will flag it). If the layout is
  already full, skip the image and give the space to the content (e.g. expand the
  cards). Reserve images for slides with room: covers, section dividers, a light
  statement slide, or a dedicated image slot.

## Text overrun
The build verifies text fit (the gate's `overflow` check measures every fixed
text box against its real area, insets included). When a slide overruns:
1. First try to shorten — tighten wording, cut a bullet, drop a redundant line.
2. If it still overruns and can't be shortened without losing the point, **choose
   the layout that actually fits the blocks** — there is no single right shape.
   Consider the full menu and pick by fit, not by habit: a different column count
   (e.g. four cards as 2×2 instead of a 1×4 strip, or vice-versa), a balanced
   split when a graphic crowds the text (chart and cards each get half rather than
   60:40), a **table** for dense parallel data, fewer items per slide, or a
   **split across two slides**. The runtime's card grid already re-flows to a
   taller shape when cards don't fit their area; your job is the higher-level
   choice — the split, the block order, and whether everything belongs on one
   slide.
3. **Remove a non-essential image placeholder** to free space before sacrificing
   content — an image is optional, the content is not.
4. Never deliver a slide whose text overruns its box. Re-run the gate until the
   overflow check is clean.
- Cite sources in a `footnote`; never invent figures or quotes.
- Label illustrative or estimated data explicitly.
- Charts: one message per chart. On a single-chart slide the action title carries
  it (no embedded chart title). On a multi-chart/dashboard slide, give EACH chart
  its own `heading` (+ optional `subheading`) — the runtime renders these as a
  text shape above the chart in the house Heading/Subheading style, never an
  embedded chart title. Keep data labels on so values are visible. Pick the chart
  type from the supported set; keep series ≤ 5 where possible.

## Adornments
- `conclusion` = one-line takeaway on a content slide. `footnote` = source /
  disclaimer. Both are bottom-anchored and expand upward.
- Never place either on cover/structural/legal layouts (Title Slide, Section,
  Title Slide with Picture, Contents, Confidentiality, Qualification, Backcover).

## Consistency & accessibility
- Consistent terminology, capitalisation, and number formats across the deck.
- Sufficient contrast; do not rely on colour alone to convey meaning.
- Spell out acronyms on first use for mixed audiences.
