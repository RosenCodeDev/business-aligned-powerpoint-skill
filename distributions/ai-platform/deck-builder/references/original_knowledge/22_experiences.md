# Experiences — lessons the builder reads before every deck

Consult this at build time (Phase 6) to avoid known, repeatable mistakes. The
machine-readable **gate** (`gate_result.json`) enforces most of these — but
reading them first means fewer rebuild loops. When you hit a *new* repeatable
mistake, tell the user to add a one-line entry here (the GPT can't persist files
itself, so the human curates this list).

## Icons (gate: `icon_coverage`)
- Icons attach **only** to `show_columns` columns and `dashboard` KPIs — add one
  to **every** such item (default-on). Use a keyword from the bundled set; omit
  only when no concept fits, and say why.
- `show_process`, `pyramid`, `cycle`, `show_growing_steps` and other diagram
  intents do **not** have icon slots — don't add `icon` there (it's dropped).
- Never put icons on cover/structural/legal layouts.

## Images (gate: `image_slots`)
- Image-bearing slots: `introduce_topic.image` (cover), `introduce_person.photo`
  (bio), and `compose` `image` blocks. Default to a **swappable** `REPLACE:<name>`
  placeholder unless the user supplied an asset or turned generation on.
- One source can be reused with different crops via `aspect`/`crop` — register it
  once in deck-level `images`, don't invent several images.
- Images are decorative only — **never** carry data, numbers, or claims.

## Action titles (gate: `action_titles`)
- Content-slide titles must be **insight sentences** ("Digital now controls 60%
  of CAC"), not topic labels ("Market Overview"). The gate fails titles under 4
  words that contain no number. Covers/section dividers are exempt.

## Overflow (gate: `overflow`)
- If the gate flags overflow, **shorten the text or split the slide** — never
  rely on shrink-to-fit below the brand minimum size. Dense tables/bullets split
  automatically; trust the runtime rather than cramming.

## Rendering / QA blind spots
- `treemap` (native chartEx) renders **blank in headless/non-PowerPoint** previews
  but is correct in PowerPoint — don't "fix" a treemap because a headless
  screenshot looks empty; verify in PowerPoint.
- Unknown JSON keys are **silently dropped** — use only the documented schema in
  `01_readme_deck_system.md`. If a feature seems missing, check the schema before
  assuming the runtime can't do it.

## Content integrity (gate: `sources`)
- Don't fabricate data, figures, or citations. Pull every fact from
  `research.json`; cite a `source`/`footnote` on content slides.
- `longform` slides use `paragraphs`, not bullets.

## The gate itself (non-negotiable)
- After building, the runtime writes `gate_result.json`. **Read it.** `passed`
  is a Python boolean — you cannot declare done by self-assessment. If
  `passed:false`, fix every `fail_items` entry and rebuild until `passed:true`.
  Warnings (`warn_items`) don't block delivery but should be surfaced to the user
  (e.g. "3 image placeholders to fill").

## Icon & image style (current)
- Icons are **fine-line** (single-weight navy strokes), placed on top of
  `show_columns` columns and centered on top of each `dashboard` KPI card.
- **Image style is photorealistic for BOTH paths, from one source of truth**
  (`_PHOTO_RULES` / `build_image_prompt` in `images.py`): "real photography…
  no CGI, no illustration". Placeholders render a copy-paste ChatGPT prompt that
  forces this; Generate & embed must build its prompt the same way (see
  `02_runtime_bootstrap.md`) — sending the bare description makes the tool drift
  to illustration. Tell the user (placeholder mode): copy the prompt line into
  ChatGPT, generate, then drop the image into the `REPLACE:` box. Give every
  image source a short `prompt`/description so the prompt is specific.

## Composite components (new)
Prefer the named components over `compose`: `stat_callout` (big numbers),
`icon_rows` (icon+heading+text list),
(tier labels), `compare` (pros/cons check-cross). Schemas in
`01_readme_deck_system.md` / `20_slide_design_capability_map.md`. Titles still
must be insight sentences (the gate checks them).

## Density, icons, timeline (specs)
- **Density**: every content slide carries a substantive point set OR a visual.
  A would-be 3-bullet slide should gain an image/graphic/stat (`stat_callout`,
  `icon_rows`, a chart) or be merged. The gate's `density` warning flags it; the
  Deck Profile sets the target (`13_intent_modes.md`).
- **Icons**: fine-line, 1pt outline, **left-aligned** above the heading (aligned
  with the content beneath), navy.
- **Timeline**: labels left-aligned (date=sub-heading, title/desc=body), default
  before/after spacing, optional left-aligned icon per milestone.

## Accents & component flexibility (added)
`sticker` (amber highlight) is available. Components are
variadic — use any number (stat cards wrap to a grid). Prefer a named component
or accent over `compose`; reach for `compose` only to mix several on one slide.

## Compose blocks & infographics (added)
Every component and the `infographic` (funnel/gauge/venn) are now `compose` block
kinds — use `compose` to place any number of them, mixed with charts/text, in any
arrangement. Reach for a standalone intent for a single component filling a slide;
use `compose` to combine several. Infographics are native editable shapes.

## Removed + grid/text rules (latest)
Brackets/braces, filled-arrow banners, and label_stack were removed — do not offer them. Two-pane slides are grid layouts (`equal` = 2-column grid; `split` = 3-column grid with a 2-column span) — same proportions as `compose.grid`, no separate ratio rule. Card/component text is Heading 12pt + body 12pt in default navy; card icons are 0.2" inset, 0.5", text at 0.9".

## Voice (gate: `voice`)
- The gate flags banned vague-active verbs (leverage, enable, enhance, transform,
  optimize, empower, facilitate, synergy, seamless) and generic claims
  (best-in-class, game-changing, drive value). On a `voice` warning, rewrite with a
  specific, evidence-backed verb — "cut unit cost 7%", not "optimize spend". Source

## Design (gate: `design`)
- `design` warnings are advisory chart/layout choices: a pie/doughnut past ~6 slices
  (use a bar chart to rank categories) or a small text-only table (use
  `show_columns`/cards — a grid is for dense numeric data). The deeper aesthetic
  judgment (density, busyness, coherence) is scored by the eval harness, not the gate.
