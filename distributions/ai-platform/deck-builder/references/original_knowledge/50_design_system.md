# OW Presentation GPT — Design System

**Runtime v2.6.18. Generated from code** (`Tokens`, `BRAND_COLORS`,
`BRAND_RULES`, `BULLET_LEVELS`). Do not hand-edit — regenerate with
`generate_deck.py --list-tokens`. This is the single source of truth for every
quantitative design fact; knowledge files reference it rather than restating it.

Fonts and the colour palette come from the `ow_default.pptx` theme (Marsh Serif
major / Noto Sans minor; midnight blue `#000F47`, gold `#FFBF00`, light blue
`#CEECFF`, cream `#F7F3EE`, warm greys `#7B7974` / `#B9B6B1`). Everything below is
enforced by the engine — the GPT never sets these.

This file is the contract between the brand and the engine. The tables are generated from live code, so they are always true; the prose is written by hand to say *why* a value exists and *when* to reach for it. Read the prose to make a judgement; trust the table for the number.

## Colours
The raw OW palette is the literal colour set; the semantic roles below reference
into it so there is one place to change a colour. Reach for a *role*, not a hex.

**OW palette (literal)**

| Name | Hex | Use for |
| --- | --- | --- |
| `midnightblue` | `#000F47` | primary text / strong fill |
| `cream` | `#F7F3EE` | default decorative fill |
| `skyblue` | `#82BAFF` | mid blue (charts, secondary fills) |
| `lblue` | `#CEECFF` | subtle highlight |
| `gold` | `#FFBF00` | text highlight / accent rule |
| `grey` | `#7B7974` | secondary text |
| `lgrey` | `#B9B6B1` | hairlines and dividers |
| `pale` | `#EBE7E2` | neutral track / pale fill |
| `white` | `#FFFFFF` | reversed text / ground |

**Semantic roles — BRAND_COLORS**

| Role | Resolves to | Via | Use for |
| --- | --- | --- | --- |
| `default_fill` | `#F7F3EE` | — | resting fill for any decorative shape (use unless emphasising) |
| `subtle_highlight` | `#CEECFF` | `accent3` | emphasis that doesn't shout |
| `strong_highlight` | `#000F47` | `accent1` | the primary attention-grab |
| `text_highlight` | `#FFBF00` | — | mark a word or a rule — not a whole shape |

Colour is addressed by *role*, never by hex, so the palette has one place to change. `default_fill` (warm cream) is the resting state for any decorative shape — reach for it unless a shape is genuinely being emphasised. `subtle_highlight` (light blue) is emphasis that doesn't shout; `strong_highlight` (midnight blue) is the primary attention-grab; `text_highlight` (gold) marks a word or a rule, not a whole shape. The gold is the same colour as the Conclusion's rule on purpose, so the eye links 'this is the point' across the deck. If a source deck arrives in an off-brand colour, rebind to one of these roles — do not carry the literal through.

## Type scale — TYPE_* (points)
| Token | Value |
| --- | --- |
| `TYPE_AUTOFIT_MIN` | 10 |
| `TYPE_AXIS` | 12 |
| `TYPE_BODY` | 12 |
| `TYPE_CARD_CAPTION` | 10 |
| `TYPE_CARD_QUOTE` | 22 |
| `TYPE_CARD_QUOTE_MARK` | 60 |
| `TYPE_CARD_VALUE` | 40 |
| `TYPE_CONCLUSION` | 18 |
| `TYPE_CONTENTS` | 16 |
| `TYPE_DIAGRAM_MIN` | 8 |
| `TYPE_EYEBROW` | 11 |
| `TYPE_FOOTNOTE` | 8 |
| `TYPE_HEADING` | 12 |
| `TYPE_INSIGHTS` | 18 |
| `TYPE_KPI` | 26 |
| `TYPE_KPI_COMPACT` | 26 |
| `TYPE_MAJOR_MIN` | 18 |
| `TYPE_MARKER` | 14 |
| `TYPE_QUOTE_MAX` | 54 |
| `TYPE_QUOTE_MIN` | 18 |
| `TYPE_TABLE_HEADER` | 12 |

Two floors: Marsh Serif (major) never below `TYPE_MAJOR_MIN`; auto-fit body/label
text never below `TYPE_AUTOFIT_MIN`.

The scale is built around two anchors and two floors. The anchors are `TYPE_BODY` (everything reads up or down from body) and `TYPE_KPI` (the display number that has to carry a slide from across a room). The floors are non-negotiable: `TYPE_MAJOR_MIN` keeps Marsh Serif large enough to stay editorial rather than fading into body copy, and `TYPE_AUTOFIT_MIN` is the point below which auto-fit stops shrinking and instead leaves the overflow visible — a deliberate signal to cut words, never a licence to render text too small to read. Reach for `TYPE_INSIGHTS` only for the one-line 'so what'; if every line is an insight, none is.

## Spacing & geometry — SPACE_* (inches)
| Token | Value |
| --- | --- |
| `SPACE_AXIS_LABEL_H` | 0.32" |
| `SPACE_CARD_ACCENT_H` | 0.07" |
| `SPACE_CARD_ICON` | 0.46" |
| `SPACE_CARD_PAD` | 0.22" |
| `SPACE_CARD_VIZ_GAP` | 0.16" |
| `SPACE_CONCL_H` | 0.55" |
| `SPACE_CONCL_LINE` | 0.3" |
| `SPACE_CONTENT_BOTTOM` | 0.2" |
| `SPACE_CONTENT_H` | 5.06" |
| `SPACE_CONTENT_W` | 12.333" |
| `SPACE_CONTENT_X` | 0.5" |
| `SPACE_CONTENT_Y` | 1.54" |
| `SPACE_GAP` | 0.25" |
| `SPACE_GAP_LG` | 0.5" |
| `SPACE_HEADING_H` | 0.3" |
| `SPACE_ICON` | 0.5" |
| `SPACE_ICON_INSET` | 0.2" |
| `SPACE_SHAPE_MARGIN` | 0.15" |
| `SPACE_TABLE_HEADER` | 0.34" |
| `SPACE_TABLE_ROW` | 0.3" |
| `SPACE_TL_LABEL_H` | 0.5" |

Spacing is deliberately coarse so slides can't drift into bespoke gutters. `SPACE_GAP_LG` is the default gutter for grids and two-pane splits; `SPACE_GAP` is the fallback used *only* when the large gutter would breach a minimum column width. The content box (`SPACE_CONTENT_X/Y/W/H`) clears a two-line title on purpose — never push content above `SPACE_CONTENT_Y` to win space, because that is the line that stops titles and bodies colliding (a regression we have hit before). Card internals key off `SPACE_CARD_PAD`; keep them there so every card breathes identically.

## Paragraph space-after — PARA_* (points)
| Token | Value |
| --- | --- |
| `PARA_BULLET` | 4 |
| `PARA_HEADING` | 2 |
| `PARA_PROSE` | 6 |
| `PARA_QUOTE_GAP` | 12 |
| `PARA_SUBHEAD` | 8 |

Paragraph spacing does the work that blank lines would otherwise do. `PARA_BULLET` separates list items; `PARA_PROSE` is the looser setting for running text; `PARA_SUBHEAD` opens air above a sub-heading so it reads as a break. Never simulate spacing with empty paragraphs — it breaks auto-fit's height maths.

## Text-box insets — INSET_* (points)
| Token | Value |
| --- | --- |
| `INSET_R` | 5 |
| `INSET_TOP` | 0 |
| `INSET_X` | 2 |

Insets stay near zero on purpose. Text boxes that carry no fill use zero side margins so the text aligns to the true grid edge; a non-zero inset there would make a 'left-aligned' block look indented. `INSET_R` leaves a hair of room on the right so wrapped lines don't kiss a border.

## Strokes / outlines — STROKE_* (points)
| Token | Value |
| --- | --- |
| `STROKE_AXIS` | 0.75 |
| `STROKE_HAIRLINE` | 0.75 |
| `STROKE_PANEL` | 1.5 |
| `STROKE_RULE` | 0.75 |
| `STROKE_W` | 0.75 |
| `STROKE_W_HEAVY` | 0.75 |
| `STROKE_W_MED` | 0.75 |

A weight of `0` means no outline; this is the one place to change shape borders.

There is essentially one stroke weight in this system — `STROKE_HAIRLINE` (and its aliases) at a uniform hairline — because a deck of mixed line weights reads as noise. The single sanctioned exception is `STROKE_PANEL`, the one heavier rule on the key-message panel, which earns its weight by being rare. A weight of 0 means *no* border; that is the intended way to remove a box outline, not a near-zero hairline.

## Charts — CHART_* (chart-specific constants)
| Constant | Value |
| --- | --- |
| `CHART_LINE_WEIGHT_EMU` | 9525 EMU (0.75 pt) |
| `CHART_LINE_SERIES_EMU` | 28575 EMU (2.25 pt) |
| `CHART_DOUGHNUT_HOLE_PCT` | 75% |
| `CHART_GRIDLINE_COLOR_HEX` | `D1CEC9` |

Chart chrome is quiet and the data is loud — the deliberate contrast between `CHART_LINE_WEIGHT_EMU` (the thin axis/gridline weight) and `CHART_LINE_SERIES_EMU` (the heavier data-series stroke) is the whole point: structure recedes, the line carries. Gridlines use a warm light grey (`CHART_GRIDLINE_COLOR_HEX`), never black. The doughnut hole is kept thin (`CHART_DOUGHNUT_HOLE_PCT`) so the ring reads as a figure, not a pie. Series colour comes from the OW chart palette in order; do not hand-pick chart colours.

## Body list styles — BULLET_LEVELS (from the OW master)
| Level | Role | Size | Font | Glyph | Margin / hang | Space b/a |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Body | 12 | Noto Sans | — | 0" / 0" | 0/0pt |
| 1 | Bullet 1 | 12 | Noto Sans | • | 0.197" / -0.197" | 0/4pt |
| 2 | Bullet 2 | 12 | Noto Sans | – | 0.394" / -0.197" | 0/4pt |
| 3 | Bullet 3 | 12 | Noto Sans | - | 0.591" / -0.197" | 0/4pt |
| 4 | Heading | 12 | Noto Sans bold | — | 0" / 0" | 0/8pt |
| 5 | Subheading | 12 | Noto Sans | — | 0" / 0" | 0/0pt |
| 6 | Small primary | 26 | Marsh Serif | — | 0" / 0" | 0/0pt |
| 7 | Medium primary | 40 | Marsh Serif | — | 0" / 0" | 0/0pt |
| 8 | Large primary | 54 | Marsh Serif | — | 0" / 0" | 0/0pt |

The list styles come straight from the OW master, so they inherit rather than being re-styled per slide. Levels 0–3 are the body/bullet ladder (glyphs step from • to – to -); levels 6–8 are the Marsh Serif 'primary' display sizes. The rule that matters: the primary font is never bold (weight comes from size and the serif itself), which is why the bold flag is suppressed on those levels even if a caller asks for it.

## Alignment — Align (managed anchors + horizontal)
Table header row is bottom-left; body rows top-left; Conclusion and Footnote
bottom-left. These are the only alignments set from variables; diagram-internal
alignments remain renderer-local.

| Variable | Value |
| --- | --- |
| `LEFT` | `LEFT (1)` |
| `CENTER` | `CENTER (2)` |
| `RIGHT` | `RIGHT (3)` |
| `TOP` | `TOP (1)` |
| `MIDDLE` | `MIDDLE (3)` |
| `BOTTOM` | `BOTTOM (4)` |
| `TABLE_HEADER_ANCHOR` | `BOTTOM (4)` |
| `TABLE_BODY_ANCHOR` | `TOP (1)` |
| `TABLE_H` | `LEFT (1)` |
| `CONCLUSION_ANCHOR_XML` | `b` |
| `FOOTNOTE_ANCHOR_XML` | `b` |
| `FOOTNOTE_H` | `LEFT (1)` |

Only the alignments that recur across slides are managed here; everything inside a diagram stays renderer-local so one timeline tweak can't shift every table. The managed set encodes the house habits: table headers sit bottom-left (so a wrapped header grows upward off the rule), body cells top-left, and both the Conclusion and Footnote pin bottom-left so they share a baseline.

## Hard rules — BRAND_RULES
| Rule | Value |
| --- | --- |
| `primary_font_never_bold` | `True` |
| `primary_font_min_pt` | `18` |
| `insight_body_pt` | `18` |

These are owner-set and code-enforced, not preferences. `primary_font_never_bold` and `primary_font_min_pt` protect the Marsh Serif voice; `insight_body_pt` sets the floor that makes an insight callout read as a statement. Code upholds them even when a caller asks otherwise — that is the point of putting them here rather than in prose.


## Components — block inventory (generated)
Each recurring block declares the content slots it consumes and the design tokens it binds. Bindings are *references*, resolved live; the linter checks them for broken refs, orphaned palette roles, and WCAG contrast. The prose says when to reach for each.

### `conclusion`
The bottom-pinned key-takeaway line with the amber left rule.

The bottom-pinned takeaway with the amber left rule — the line the reader should leave with. Keep it to ~one line; it grows upward from a fixed baseline, so a long conclusion eats the content area rather than overflowing. Pair it with a `footnote` for the source.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `conclusion` | string | yes | ~one-line takeaway |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `body_type` | `{Tokens.TYPE_CONCLUSION}` | `18` |
| `body_color` | `{palette.midnightblue}` | `#000F47` |
| `rule_color` | `{BRAND_COLORS.text_highlight}` | `#FFBF00` |
| `height` | `{Tokens.SPACE_CONCL_H}` | `0.55` |

**Overrides:** —  
**Contrast (WCAG):** —

### `icon_card`
Icon + heading + body text card; the default grid cell.

The default grid cell: icon, heading, body. **Use when** content is a set of parallel points (three to four) that each want a glyph and a line. If the points have no real icon, that is usually a sign the content is a list, not a card grid — reach for bullets instead of forcing decorative icons.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `icon` | string | yes | icon keyword shown top-left |
| `heading` | string | yes | card heading |
| `body` | string | no | supporting line(s) |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `fill` | `{BRAND_COLORS.default_fill}` | `#F7F3EE` |
| `heading_type` | `{Tokens.TYPE_HEADING}` | `12` |
| `body_type` | `{Tokens.TYPE_BODY}` | `12` |
| `heading_color` | `{palette.midnightblue}` | `#000F47` |
| `body_color` | `{palette.midnightblue}` | `#000F47` |
| `icon_box` | `{Tokens.SPACE_CARD_ICON}` | `0.46` |
| `pad` | `{Tokens.SPACE_CARD_PAD}` | `0.22` |

**Overrides:** `fill`  
**Contrast (WCAG):** `heading_color` on `fill` = 16.4:1 (AA); `body_color` on `fill` = 16.4:1 (AA)

### `insight_panel`
The strong short-statement callout (Marsh Serif, 18pt floor) with the amber rule — the 'signal' on split layouts.

**Use when** a split layout needs its 'so what' stated as a single sentence beside the evidence. It is the only place Marsh Serif appears at the insight size with the amber rule, so it should be rare — one per slide at most, or it stops signalling.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `insight` | string | yes | one-sentence signal / 'so what' |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `body_type` | `{BRAND_RULES.insight_body_pt}` | `18` |
| `body_color` | `{palette.midnightblue}` | `#000F47` |
| `rule_color` | `{BRAND_COLORS.text_highlight}` | `#FFBF00` |
| `rule_w` | `{Tokens.STROKE_PANEL}` | `1.5` |

**Overrides:** —  
**Contrast (WCAG):** —

### `kpi_card`
A single big-number stat tile: value, label, optional delta.

**Use when** a slide needs a small set of headline numbers that each stand alone — three to four KPIs in a grid, or a single hero figure. Prefer it over a `dashboard` when the numbers are the message rather than a supporting scoreboard. The `fill` and `accent` overrides exist to pick a *different OW role* (e.g. a light-blue emphasis tile), not to introduce an off-palette colour — a fill that isn't a palette role will trip the contrast and orphan lints.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `value` | string | yes | the headline number, e.g. '+150%' |
| `label` | string | yes | what the number measures |
| `delta` | string | no | movement vs a baseline, e.g. '▲ 12 pts' |
| `icon` | string | no | icon keyword shown top-left |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `fill` | `{BRAND_COLORS.default_fill}` | `#F7F3EE` |
| `value_type` | `{Tokens.TYPE_CARD_VALUE}` | `40` |
| `label_type` | `{Tokens.TYPE_BODY}` | `12` |
| `caption_type` | `{Tokens.TYPE_CARD_CAPTION}` | `10` |
| `value_color` | `{palette.midnightblue}` | `#000F47` |
| `label_color` | `{palette.midnightblue}` | `#000F47` |
| `pad` | `{Tokens.SPACE_CARD_PAD}` | `0.22` |
| `accent_h` | `{Tokens.SPACE_CARD_ACCENT_H}` | `0.07` |

**Overrides:** `fill`, `accent`  
**Contrast (WCAG):** `value_color` on `fill` = 16.4:1 (AA); `label_color` on `fill` = 16.4:1 (AA)

### `quote_card`
A pull-quote tile with an oversized opening quote mark.

**Use when** a verbatim voice earns its own tile — a customer line, an expert sentence. One per slide; the oversized mark is the visual, so keep the quote tight. The light-blue mark is deliberately quiet so the words, not the punctuation, carry.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `quote` | string | yes | the quotation text |
| `attribution` | string | no | speaker / source |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `fill` | `{BRAND_COLORS.default_fill}` | `#F7F3EE` |
| `quote_type` | `{Tokens.TYPE_CARD_QUOTE}` | `22` |
| `mark_type` | `{Tokens.TYPE_CARD_QUOTE_MARK}` | `60` |
| `caption_type` | `{Tokens.TYPE_CARD_CAPTION}` | `10` |
| `quote_color` | `{palette.midnightblue}` | `#000F47` |
| `mark_color` | `{palette.lblue}` | `#CEECFF` |
| `pad` | `{Tokens.SPACE_CARD_PAD}` | `0.22` |

**Overrides:** `fill`  
**Contrast (WCAG):** `quote_color` on `fill` = 16.4:1 (AA)

### `stat_card`
A stat with a one-line callout — like kpi_card but caption-led.

**Use when** the figure needs a sentence to land — '€2.4bn, the cost of doing nothing'. Caption-led, so it carries one stat with context rather than a bare number. For several bare numbers side by side, use `kpi_card` instead.

**Slots**

| Slot | Type | Required | Note |
| --- | --- | --- | --- |
| `value` | string | yes | the figure |
| `label` | string | yes | the callout sentence under the figure |
| `icon` | string | no | icon keyword |

**Bound tokens**

| Role | Reference | Resolves to |
| --- | --- | --- |
| `fill` | `{BRAND_COLORS.default_fill}` | `#F7F3EE` |
| `value_type` | `{Tokens.TYPE_CARD_VALUE}` | `40` |
| `label_type` | `{Tokens.TYPE_BODY}` | `12` |
| `value_color` | `{palette.midnightblue}` | `#000F47` |
| `label_color` | `{palette.midnightblue}` | `#000F47` |
| `pad` | `{Tokens.SPACE_CARD_PAD}` | `0.22` |

**Overrides:** `fill`, `accent`  
**Contrast (WCAG):** `value_color` on `fill` = 16.4:1 (AA); `label_color` on `fill` = 16.4:1 (AA)

## Changing the system
Edit the value in `Tokens` / `BRAND_COLORS` / `BRAND_RULES`, run `pytest`
(`test_tokens_are_single_source_of_truth` + the invariant tests guard it), rebuild
the runtime zip, and regenerate this file with `--list-tokens`. Component slots
and bindings live in `design_components.py`; their rationale in `design_prose.py`.

