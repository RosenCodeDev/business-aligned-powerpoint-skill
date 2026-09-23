# Storyline Logic

How the argument inside a deck is built so it lands quickly with a decision-maker.
This file governs the **vertical** logic of a deck — the line of reasoning that runs
from the core message down to the evidence. It is applied at the outline step
(Phase 4), after the deck shape has been chosen (see `14_content_structures.md`) and
before any slides are generated.

This is not a new analysis step. It only organizes what is already captured in
`/mnt/data/research.json`. It never introduces claims, figures, or recommendations that the
sources do not support.

## Core principle

Lead with the answer, then support it. A reader who stops after the first minute
should already know the recommendation and the one reason it holds. Build the
support as a pyramid: one governing message at the top, a small set of
mutually distinct supporting arguments beneath it, and the evidence under each.
Every supporting argument must be necessary to the message, and together they
must be sufficient to carry it — no overlap, no gaps.

## Workflow (runs at the start of Phase 4)

1. Restate the audience, the decision they must make, and the action you want from
   them. Pull this from the Phase 1 answers (Intent Mode, audience).
2. Write the **core message** as a single sentence. If it needs an "and", it is
   probably two messages — split or pick the dominant one.
3. Lay out the **pyramid**: the supporting arguments under the core message, and
   the evidence (from `/mnt/data/research.json`) under each argument. Mark any argument the
   sources do not yet support as a gap rather than filling it.
4. Choose the **opening pattern** by Intent Mode (table below).
5. Derive the **headline sequence** from the pyramid — one headline per slide, in
   the order the argument unfolds. The headlines, read in order on their own,
   must tell the whole story. **Mark the key (anchor) slides** with a ★: the
   opening core-message slide, the one slide that carries each supporting
   argument, each deep-dive/section opener, and the close. These are the slides
   that hold up the argument; the rest are evidence and detail. The pyramid
   already names them — this is surfacing what the spine contains, not a new
   judgement.
6. Note the **likely objections** a skeptical reader will raise, and where in the
   deck each is answered (often an appendix slide or a pre-empting line).
7. **Group the headline sequence into sections and mark the dividers.** If the
   deck has distinct major parts — a deep dive per item, a multi-part comparison,
   before/after, or workstream-by-workstream — open each part with a
   `section_divider`. A multi-report or multi-entity comparison gets a divider per
   entity (e.g. "Deep Dive: CEO Agenda", "Deep Dive: CFO Agenda"). Do not fold a
   section opener into a content slide; the divider is what makes a long deck
   navigable.

## Sections and slide count

Section dividers are structural, not content. **A requested slide count
(`~N slides`) counts CONTENT slides only** — the cover, contents, section
dividers, and back/closing structural pages never count against `N`. Adding a
divider is therefore free: never drop one, or fold it into a content slide, to
hit a number. If the brief asks for ~12 slides and the story has three sections,
the deck is ~12 content slides **plus** the cover, three dividers, and back page.

## Opening pattern by Intent Mode

| Intent Mode | Opening pattern | What leads |
|---|---|---|
| Recommend | Pyramid, recommendation first | The recommendation, then why |
| Decide | Pyramid + explicit decision ask | The decision required, then the case |
| Align | SCQA (Situation–Complication–Question–Answer) | Shared context, then the ask and next steps |
| Inform | Pyramid, finding first | The headline finding, then detail |
| Inspire | Transformation arc | From-state → to-state → the path |

Use SCQA whenever the audience needs context or a sense of urgency before the
answer will land; use straight pyramid when they already know the context.

## Output: the storyline spine

Produce this before the slide-by-slide outline, and get it approved as part of the
outline approval loop:

```
Core message:   [one sentence]
Pyramid:
  - Argument 1  → evidence / gap
  - Argument 2  → evidence / gap
  - Argument 3  → evidence / gap
Opening pattern: [from table]
```

The Phase 4 outline (**# | Key | Takeaway headline | Objective**) is then derived
directly from this spine — each headline is a node of the pyramid, in narrative
order. The **Key** column carries ★ for the anchor slides identified in step 5.

## Key slides get the visual investment

A deck does not deserve equal visual weight on every slide; it deserves the most
on the slides that carry the argument. **Every ★ key slide must lead with a
primary visual** — the strongest supported design for its content: a chart, a KPI
dashboard, a diagram, a hero stat, or an image (see `20_slide_design_capability_map.md`
for what's visual). A key slide is never text-only. Supporting/evidence slides
may stay lean. The close is *always* a key slide — render it as cards, a summary
diagram, or a hero stat, never a paragraph list. This concentrates design effort
where the argument lives instead of spreading it evenly; it is applied at build
(Phase 6).

## Quality bar

- The first slide reveals the recommendation or the headline finding.
- The takeaway headlines, read top to bottom on their own, convey the argument.
- Supporting arguments are mutually distinct and jointly sufficient.
- Every claim traces to `/mnt/data/research.json`; gaps are flagged, never invented.
- Setup and throat-clearing that does not move the decision is removed.

## When to apply with a light touch

Full pyramid discipline is most valuable for the **`consulting`** profile and
decision audiences. For **`longform`**, keep the core-message-first discipline but
allow a flowing, paragraph-led build rather than a strict headline ladder; for
internal or execution-focused audiences, the pyramid can be broader and flatter
with more context and execution detail.
