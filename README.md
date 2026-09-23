# Deck Builder Skill

This repository packages the recovered **Deck Builder** Custom GPT as an installable Codex/Agent Skill. It preserves the original template-native PowerPoint runtime, the 14 exact knowledge files, and the owner-authored interview, storyline, generation, and quality-gate workflow.

> Install the distribution folder, not the repository root: `distributions/ai-platform/deck-builder`.

## What is preserved

- Runtime version 2.6.18 and its bundled Oliver Wyman PowerPoint template.
- Original intent, content-structure, storyline, design, icon, and voice guidance.
- The three-question interview and two explicit approval checkpoints.
- Runtime-only PPTX generation and the non-overridable `gate_result.json` check.
- Placeholder-first image behavior and evidence/citation safeguards.

The disposable claims-intake test artifacts are intentionally excluded.

## Repository layout

```text
distributions/ai-platform/deck-builder/  Installable skill
scripts/validate_package.py              Integrity and structure checks
scripts/validate-and-package.ps1         Validation and release ZIP creation
tests/                                   Wrapper and package tests
```

## Validate

```powershell
python scripts/validate_package.py
python -m unittest discover -s tests -v
```

## Package

```powershell
pwsh ./scripts/validate-and-package.ps1
```

The release archive is written to `dist/deck-builder.zip`.

The validation workflow runs the same validation and packaging command on
pushes, pull requests, and manual dispatches, and uploads the ZIP as a workflow
artifact. Pushing a version tag such as `v1.0.0` runs the release workflow,
revalidates the package, and publishes `deck-builder.zip` as a GitHub Release
asset.

## Rights and portability

The recovered package does not include a license grant for the runtime, template, embedded fonts, icons, or Oliver Wyman branding. Confirm authorization before redistribution. Missing or substituted fonts can alter wrapping and visual output even when the runtime gate passes. See `references/migration/LICENSE_AND_ORIGIN.md` in the skill distribution.
