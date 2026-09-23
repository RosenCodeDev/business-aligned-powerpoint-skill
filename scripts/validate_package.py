#!/usr/bin/env python3
"""Validate the Deck Builder skill package without modifying it."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "distributions" / "ai-platform" / "deck-builder"
RUNTIME_HASH = "c595e17c097d16aa33880193fceec3928e7a08cfcca603ffa82f0a03a2f7663d"
KNOWLEDGE_HASHES = {
    "01_readme_deck_system.md": "d8560170800b7e1834b294d6729563eb0ef73b8c5426e5a1829436a3c9998828",
    "02_runtime_bootstrap.md": "a592b8155294704803c64c5e7e4762e224643bdf6868d2783c9db8de22c741f7",
    "11_presentation_standards.md": "81f5396f5b98f8c47093a5259686b61d80aa97a721bf02d51116b4bddd3c8a86",
    "12_brand_guidelines.md": "5844ea3f02255509bad92b3a579a9d1ed3f971fdfc8316816c71afe505ae348c",
    "13_intent_modes.md": "2709ff2ccaecf9de10d5eef4957997471ce1591f8463bf54fe6c8fdadbcefa86",
    "14_content_structures.md": "756bd2b053f02dfb13874540f1e433e947a5028aaafe3515f1cfdabf853d1f0f",
    "15_storyline_logic.md": "0d7adc5a55de050ac7f3e9ee09e146be693f94834462d36c95da128dc18bb678",
    "16_deck_spec_authoring.md": "b8c5c3ff311fe549cefd1ce37ad831cab0e9b254be490fbdf139736491da05f2",
    "20_slide_design_capability_map.md": "122fbfb0d9ddb0f46829756441dcd290b91d3d519056944c36498b774d765934",
    "21_slide_design_selection_guide.md": "354b9be2abe21ee48f3a9aa6c17b53f139cc8dba381d2fa1fd77f5fd194dc8be",
    "22_experiences.md": "5caaf20bea8417dececde185f3980df7126b5491977541e6845cc5943fbcb87b",
    "23_icon_index.md": "b681eb802a247910ae89c4886156a33a0f9766f3a88ea4fabaf33f46feee115d",
    "50_design_system.md": "31142ec472eef1df0edef3a9e46ad0b25e83e84d5eb45c13fcb003e1484bf63f",
    "60_voice_system.md": "b360dd0edc699db9ae56f783d69224043cfee79cf2415a37784ab6d32c768603",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    required = [
        SKILL / "SKILL.md",
        SKILL / "agents" / "openai.yaml",
        SKILL / "requirements.txt",
        SKILL / "scripts" / "runtime_adapter.py",
        SKILL / "assets" / "deck_system_runtime_clean.zip",
        SKILL / "references" / "resource_manifest.json",
    ]
    for path in required:
        require(path, errors)

    skill_file = SKILL / "SKILL.md"
    if skill_file.is_file():
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---\nname: deck-builder\n"):
            errors.append("SKILL.md frontmatter must start with name: deck-builder")
        if "description:" not in text.split("---", 2)[1]:
            errors.append("SKILL.md frontmatter has no description")

    runtime = SKILL / "assets" / "deck_system_runtime_clean.zip"
    if runtime.is_file():
        actual = digest(runtime)
        if actual != RUNTIME_HASH:
            errors.append(f"runtime hash mismatch: {actual}")
        else:
            with zipfile.ZipFile(runtime) as bundle:
                names = set(bundle.namelist())
                for member in ("src/generate_deck.py", "src/runtime.py", "ow_default.pptx", "requirements.txt"):
                    if member not in names:
                        errors.append(f"runtime archive missing {member}")

    knowledge = SKILL / "references" / "original_knowledge"
    for name, expected in KNOWLEDGE_HASHES.items():
        path = knowledge / name
        require(path, errors)
        if path.is_file() and digest(path) != expected:
            errors.append(f"knowledge hash mismatch: {name}")

    forbidden = list(SKILL.rglob("*claims-intake*"))
    if forbidden:
        errors.append("claims-intake test artifacts must not be packaged")

    if errors:
        print("Package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(json.dumps({
        "skill": str(SKILL),
        "runtime_sha256": RUNTIME_HASH,
        "exact_knowledge_files": len(KNOWLEDGE_HASHES),
        "claims_test_artifacts": 0,
        "status": "valid",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
