---
name: deck-builder
description: Create executive-quality Oliver Wyman PowerPoint decks with the recovered template-native runtime. Use for new PPTX decks, precise deck specifications, or deck-generation requests that should follow the Deck Builder interview, storyline, voice, design, and hard quality-gate workflow.
---

# Deck Builder

Build editable `.pptx` decks through the bundled Deck Builder runtime. Preserve the recovered Custom GPT's workflow and template behavior.

## Non-negotiable runtime rules

- Use `scripts/runtime_adapter.py` for runtime preflight, linting, and generation.
- Do not substitute the generic presentation engine, `pptxgenjs`, or hand-written `python-pptx` generation. The bundled runtime already owns the template, layout compiler, charts, diagrams, icons, text metrics, and gate.
- Treat the skill directory and bundled resources as immutable. Write research, specs, images, PPTX files, and gate results into the user's task workspace.
- Never claim a deck was built unless the PPTX exists and `gate_result.json` contains the boolean `"passed": true`.
- Do not fabricate facts, figures, citations, quotations, images, or source support. Label illustrative material clearly.
- Keep the original runtime ZIP byte-identical. Do not patch extracted runtime code during ordinary deck work.

## Interaction workflow

### Direct-build exception

If the user supplies a precise per-slide specification or a deck JSON/YAML file, map it to the runtime deck specification, confirm once, then preflight and build. Skip the interview and outline phases.

### Phase 1: discovery

For an ordinary request, ask one question per message and perform no tools or source analysis between questions:

1. Acknowledge the goal in one sentence, say that two more questions will precede the outline, then ask: **What's the deck about, and do you have source material to upload or should I research it?**
2. Ask: **Who's it for, and the one thing they should think or do afterward?** Infer a missing audience or takeaway and confirm it later.
3. Ask the image choice: **No images / Placeholders (default) / Generate and embed real photos.**

Infer deck intent, voice, depth, and soft content-slide count from the answers. Use `consulting` for presented/decision-oriented audiences and `longform` for read/report-oriented audiences unless the user overrides it. Open each section with `section_divider`. `~N slides` means content slides; structural slides and runtime overflow splits do not count toward that soft target.

### Phase 2: plan confirmation

State the topic, audience, intended takeaway, inferred intent, `voice_style` with a reason, soft length, source approach, and image mode. Ask the user to change anything or reply **Go**. Revise and reconfirm until approved. Do not run tools yet.

### Phase 3: prepare

After **Go**, run:

```text
python <skill>/scripts/runtime_adapter.py preflight --workspace <task-workspace>
```

Stop if preflight does not print `RUNTIME OK v2.6.18`.

Read only the phase-relevant exact references:

- `references/original_knowledge/11_presentation_standards.md`
- `references/original_knowledge/12_brand_guidelines.md`
- `references/original_knowledge/13_intent_modes.md`
- `references/original_knowledge/14_content_structures.md`
- `references/original_knowledge/60_voice_system.md`

Analyze supplied sources once into `<task-workspace>/research.json`. Preserve findings, evidence, figures, source locations, assumptions, and gaps. Research current facts only when the user requests research or the task requires current information, and cite the sources used.

### Phase 4: storyline and outline

Read `references/original_knowledge/15_storyline_logic.md`. Propose the supported deck shape, one-sentence core message, supporting-argument pyramid with evidence gaps, opening approach, and a high-level slide outline. For each slide show its number, `★` when it is a key slide, takeaway title, and objective. Do not draft full slide copy or choose detailed designs yet. Ask **A) Approve  B) Revise** and wait.

### Phase 5: revision

On revision, gather the user's changes, update the spine and outline, and seek approval again.

### Phase 6: build

After outline approval:

1. Reuse `research.json`; do not re-analyze the same material.
2. Read `22_experiences.md` first, then `20_slide_design_capability_map.md`, `01_readme_deck_system.md`, `23_icon_index.md`, and `16_deck_spec_authoring.md`. Read `21_slide_design_selection_guide.md` only when design selection remains ambiguous.
3. Apply the selected voice plus the house voice. Use only supported, approximate, or documented fallback intents. Every `★` key slide needs a primary visual rather than a text-only composition.
4. Create the task-scoped deck JSON according to `16_deck_spec_authoring.md`; unknown keys are dropped, `longform` uses paragraphs, and `consulting` uses bullets. Use runtime-native image and icon fields. Icons are all-or-nothing across the relevant columns or KPIs on a slide. For real photos, use the host image-generation capability only after an explicit request; otherwise use concrete `REPLACE:<name>` placeholders. Never draw a fake photograph in code.
5. Voice-lint the draft and fix every error:

   ```text
   python <skill>/scripts/runtime_adapter.py lint-text <draft.txt> --profile <consulting|longform> --workspace <task-workspace>
   ```

6. Build with the wrapper:

   ```text
   python <skill>/scripts/runtime_adapter.py generate <deck.json> <output.pptx> --workspace <task-workspace>
   ```

7. Read the emitted `gate_result.json`. If the wrapper reports a failed gate, correct the deck JSON and rebuild until it passes. Surface meaningful warnings, including remaining image placeholders.
8. When a reliable renderer is available, inspect rendered slides for clipping, overlap, broken fonts, and blank objects. Rendering is QA only; deliver the original editable runtime-generated PPTX.

## Delivery

Return the PPTX with a compact JSON preview, and note assumptions, unresolved evidence gaps, font substitutions, and actionable gate warnings. Omit the recovered feedback URL and token estimate unless the user explicitly requests them.

## Reference routing

- Use the exact original files under `references/original_knowledge/` as the authoritative content, brand, storyline, design, intent, icon, and voice guidance.
- Consult `references/migration/CUSTOM_GPT_CONFIGURATION.md` when maintaining or auditing behavioral parity.
- Consult `references/migration/PORTABILITY_GAPS.md` for environment adaptation.
- Consult `references/migration/LICENSE_AND_ORIGIN.md` before redistributing branded assets or the runtime.
- The reconstructed claims-intake example is intentionally absent and is not a benchmark.
