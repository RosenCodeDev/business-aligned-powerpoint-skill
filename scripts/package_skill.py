#!/usr/bin/env python3
"""Create a clean Deck Builder release ZIP."""

from __future__ import annotations

from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "distributions" / "ai-platform" / "deck-builder"
DEFAULT_OUTPUT = ROOT / "dist" / "deck-builder.zip"


def include(path: Path) -> bool:
    relative = path.relative_to(SKILL)
    return "__pycache__" not in relative.parts and path.suffix != ".pyc"


def main() -> int:
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    if temporary.exists():
        temporary.unlink()
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and include(path):
                archive_name = Path(SKILL.name) / path.relative_to(SKILL)
                bundle.write(path, archive_name.as_posix())
    temporary.replace(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

