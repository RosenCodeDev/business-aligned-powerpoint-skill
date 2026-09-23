# Portability gaps

This file identifies dependencies on the original ChatGPT/Custom-GPT operating environment and the smallest concrete change needed for an equivalent local Codex/Agent Skill.

| Gap / dependency | Original behavior | Local/Codex impact | Smallest concrete adaptation |
|---|---|---|---|
| `/mnt/data` workspace | Runtime bootstrap searches `/mnt/data`, `/mnt`, cwd and extracts to `/mnt/data/ow_runtime` | Windows/local agents may not have those paths or permissions | Introduce a configurable `WORKSPACE_DIR`; default to the skill workspace, temp directory, or repository-local `.work/`; pass absolute paths |
| Lazy GPT Knowledge staging | First Code Interpreter execution causes Knowledge files to appear in `/mnt/data` | Local agents do not have this staging mechanism | Ship references/runtime beside the skill or resolve them from a configured resource directory |
| ChatGPT Code Interpreter / Data Analysis | Used to execute bootstrap, runtime, tests, file operations | A text-only agent cannot build PPTX | Require a local Python execution tool with filesystem access; fail explicitly if unavailable |
| ChatGPT image-generation tool | Explicit "Generate & embed real photos" mode calls an image model and saves images into workspace | A local Codex agent may not have image generation | Inject an image-provider adapter; if absent, force placeholder mode and disclose it |
| ChatGPT/web browsing | Research may browse and cite when requested | Offline/local environments cannot verify current facts | Inject a web/search adapter; otherwise restrict to provided sources and mark current facts unverified |
| ChatGPT-specific image prompt wording | Placeholder guidance tells a user to paste a prompt into ChatGPT | Product-specific wording may be wrong locally | Change placeholder text to the configured image generator while preserving the same photorealism rules |
| Runtime bootstrap hard-coded archive discovery | Looks for `*runtime*clean*.zip` / `*runtime*.zip` in ChatGPT-style roots | Unnecessary and brittle locally | Resolve a skill-relative extracted runtime path first; use archive bootstrap only as fallback |
| Unix font search paths | `textmetrics.py` searches `/usr/share/fonts`, `/usr/local/share/fonts`, `~/.fonts` | Windows font metrics may fall back poorly | Add `%WINDIR%\Fonts`, corporate font directories, and/or a configurable font-path list |
| Brand fonts | Marsh Serif / Noto Sans are referenced by template/theme; embedded font data may be obfuscated for metrics | Missing fonts can change wrapping and visual parity | Install/licence the fonts where permitted, or validate against approved substitutes; do not silently claim exact visual parity |
| PowerPoint-native ChartEx treemaps | Valid in PowerPoint; may appear blank in headless/non-PowerPoint renderers | Screenshot QA can falsely report failure | Exempt ChartEx treemap previews from headless visual-failure logic and verify in PowerPoint when possible |
| No universal visual renderer bundled | Runtime gate checks structure/content but does not guarantee a desktop-PowerPoint screenshot | Local visual QA may be weaker | Add an optional render stage (PowerPoint automation on Windows, LibreOffice with caveats, or approved cloud renderer) and visual diff checks |
| Current host-specific Python hook | This environment injects an unrelated spreadsheet warm-up into child Python processes | Can slow tests in this host only | For this host set `OAI_IS_JUPYTER_KERNEL=0` when running subprocess tests; do **not** make this a runtime requirement |
| External web/image provider credentials | Not stored in runtime or migration package | Research/image adapters may need credentials | Configure credentials outside the skill package via secret manager/environment; never embed them |
| Original Custom GPT editor toggles | Exact saved capability toggles are unavailable | Cannot reproduce editor UI state exactly | Treat capabilities as explicit skill prerequisites and validate at activation |
| Custom Actions/connectors | No accessible Action/OpenAPI or connector configuration | Possible hidden integrations cannot be reproduced | Human owner should inspect GPT editor and export any custom Action schemas/connectors if they exist |
| Conversation starters / GPT description | Unavailable | Onboarding text may differ | Retrieve manually from the GPT editor; they are not needed for core deck behavior |
| `research.json` fixed ChatGPT path | Exact owner workflow writes `/mnt/data/research.json` | Local workspaces differ | Write `<workspace>/research.json` and pass that path explicitly |
| Generated image paths | Exact owner workflow saves generated images under `/mnt/data` | Local paths differ | Save into `<workspace>/images/` and register absolute/skill-relative paths |
| Feedback telemetry / URL | Final response includes `[Leave your feedback](https://owy.mn/4v3C4gV)` | May be internal, expired, or inappropriate outside original deployment | Make `feedback_url` optional configuration; default to omitted unless owner explicitly preserves it |
| Token estimate in wrap-up | Original instructions request a token estimate | Token reporting may be unavailable or meaningless in other hosts | Make optional; omit if the host cannot provide a meaningful estimate |
| Oliver Wyman branding | Runtime and template hard-code OW fonts, colors, layout logic, and terminology | Skill is not brand-neutral and may be inappropriate for other organizations | Preserve only if owner has rights and wants OW parity; otherwise replace template + design tokens + brand references together |
| Template file name | Runtime examples use `ow_default.pptx` | Local package may locate assets differently | Store template path in configuration and pass it explicitly to `generate_deck.py` |
| Relative CLI assumptions | Some examples/tests assume running from runtime root | Local agent may invoke elsewhere | Always use absolute paths and set working directory explicitly |
| `python` command in some tests | Some bundled tests invoke literal `python` | Windows/venv may expose only `py` or another executable | Patch tests/process wrappers to use `sys.executable` for local CI; runtime generation itself can already be invoked explicitly |
| Macro-free deliverable expectation | Migration requires editable `.pptx`; runtime has no macro workflow | Local post-processing could accidentally add macros | Keep output extension `.pptx`; reject `.pptm`; optionally scan package for `vbaProject.bin` before delivery |
| Editable native objects | Runtime intentionally creates native charts/tables/shapes; some preview/render tools rasterize only for display | Local preview must not replace final PPTX with flattened images | Treat rendering as QA only; always deliver the original runtime-generated PPTX |
| Owner-defined approval checkpoints | Original workflow pauses at Phase 2 and Phase 4 | Autonomous agents may be tempted to continue | Encode approval gates as explicit state transitions that require user input; do not auto-approve |
| Direct-build exception | Precise per-slide specs skip Phases 1–5 after one confirmation | A generic skill may over-interview | Implement a deterministic "precise deck spec" classifier and preserve the direct-build path |
| No background execution contract | Original workflow expects synchronous build and user-visible completion | Local orchestration may schedule jobs asynchronously | Either keep synchronous execution or make job-state semantics explicit; never claim a file exists before it is built |

## Hard-coded branding and environment values that should not be copied blindly

The following should be parameterized in a portable skill unless the owner explicitly wants exact parity:

- Oliver Wyman / OW naming.
- `ow_default.pptx`.
- Marsh Serif / Noto Sans.
- OW palette and design tokens.
- `/mnt/data` and `/mnt`.
- `/mnt/data/ow_runtime`.
- `/mnt/data/research.json`.
- `/mnt/data/img_<name>.png`.
- `https://owy.mn/4v3C4gV`.
- User-facing wording that says "copy the prompt into ChatGPT."

## What can remain unchanged

If licensing and branding rights are confirmed, these behaviors are portable with minimal change:

- three-question intake,
- intent and voice classification,
- deck-shape selection,
- pyramid/storyline approval,
- section-divider semantics,
- runtime intent/deck-spec model,
- voice lint,
- non-overridable `gate_result.json`,
- no-fabrication evidence rules,
- placeholder-first image policy,
- editable native PowerPoint objects,
- fix-and-rebuild recovery loop.

## Recommended local skill resource layout

A minimal local adaptation can use:

```text
deck-builder-skill/
├── SKILL.md
├── references/
│   └── ...exact knowledge files...
├── runtime/
│   ├── src/
│   ├── ow_default.pptx
│   ├── requirements.txt
│   └── tests/
└── workspace/          # ignored / temporary
```

Then replace every `/mnt/data/...` rule with a workspace resolver:

`workspace = $DECK_BUILDER_WORKSPACE or <skill-root>/workspace`

This is the smallest change that removes the largest ChatGPT-specific dependency without changing the deck-generation logic.
