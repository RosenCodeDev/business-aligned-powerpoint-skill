#!/usr/bin/env python3
"""Portable, integrity-checking launcher for the recovered Deck Builder runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


RUNTIME_VERSION = "2.6.18"
RUNTIME_SHA256 = "c595e17c097d16aa33880193fceec3928e7a08cfcca603ffa82f0a03a2f7663d"
SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ARCHIVE = SKILL_ROOT / "assets" / "deck_system_runtime_clean.zip"
RESOURCE_MANIFEST = SKILL_ROOT / "references" / "resource_manifest.json"


class AdapterError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_workspace() -> Path:
    configured = os.environ.get("DECK_BUILDER_WORKSPACE")
    return Path(configured).expanduser().resolve() if configured else (Path.cwd() / ".deck-builder-work").resolve()


def verify_resources() -> None:
    if not RESOURCE_MANIFEST.is_file():
        raise AdapterError(f"Resource manifest missing: {RESOURCE_MANIFEST}")
    try:
        manifest = json.loads(RESOURCE_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"Cannot read resource manifest: {exc}") from exc
    if not RUNTIME_ARCHIVE.is_file():
        raise AdapterError(f"Runtime archive missing: {RUNTIME_ARCHIVE}")
    actual = sha256(RUNTIME_ARCHIVE)
    if actual.lower() != RUNTIME_SHA256:
        raise AdapterError(f"Runtime hash mismatch: expected {RUNTIME_SHA256}, got {actual}")
    declared_runtime = manifest.get("runtime_archive", {}).get("sha256", "")
    if declared_runtime != RUNTIME_SHA256:
        raise AdapterError("Resource manifest runtime hash does not match the adapter")
    for relative, expected in manifest.get("knowledge_files", {}).items():
        path = SKILL_ROOT / relative
        if not path.is_file():
            raise AdapterError(f"Knowledge file missing: {relative}")
        actual = sha256(path)
        if actual.lower() != expected.lower():
            raise AdapterError(f"Knowledge hash mismatch for {relative}: expected {expected}, got {actual}")


def safe_extract(archive: Path, destination: Path) -> None:
    destination_text = os.path.abspath(destination)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = os.path.abspath(os.path.join(destination_text, member.filename))
            if os.path.commonpath((destination_text, target)) != destination_text:
                raise AdapterError(f"Unsafe archive member: {member.filename}")
        bundle.extractall(destination_text)


def runtime_root(workspace: Path) -> Path:
    verify_resources()
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    target = workspace / f"runtime-{RUNTIME_VERSION}-{RUNTIME_SHA256[:12]}"
    marker = target / ".runtime-sha256"
    if marker.is_file() and marker.read_text(encoding="utf-8").strip() == RUNTIME_SHA256:
        return target

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=False, exist_ok=False)
    try:
        safe_extract(RUNTIME_ARCHIVE, target)
        required = [target / "src" / "generate_deck.py", target / "src" / "runtime.py", target / "ow_default.pptx"]
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise AdapterError("Runtime archive is incomplete: " + ", ".join(missing))
        marker_path = target / ".runtime-sha256"
        marker_path.write_text(RUNTIME_SHA256 + "\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise
    return target


def runtime_command(root: Path, *args: str) -> list[str]:
    return [sys.executable, "-X", "utf8", str(root / "src" / "generate_deck.py"), *args]


def run_runtime(root: Path, *args: str) -> int:
    env = os.environ.copy()
    source = str(root / "src")
    env["PYTHONPATH"] = source + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    completed = subprocess.run(runtime_command(root, *args), cwd=root, env=env, check=False)
    return completed.returncode


def read_gate(output: Path) -> dict:
    gate_path = output.resolve().parent / "gate_result.json"
    if not gate_path.is_file():
        raise AdapterError(f"Runtime did not write gate result: {gate_path}")
    try:
        result = json.loads(gate_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdapterError(f"Cannot read gate result {gate_path}: {exc}") from exc
    if not isinstance(result.get("passed"), bool):
        raise AdapterError(f"Gate result has no boolean 'passed': {gate_path}")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"deck-builder adapter {RUNTIME_VERSION}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def workspace_arg(command: argparse.ArgumentParser) -> None:
        command.add_argument("--workspace", type=Path, default=default_workspace())

    workspace_arg(subparsers.add_parser("preflight", help="Verify and stage the exact runtime."))
    workspace_arg(subparsers.add_parser("info", help="Print runtime identity and resolved paths as JSON."))

    for name in ("list-intents", "list-capabilities", "list-voice"):
        workspace_arg(subparsers.add_parser(name, help=f"Run runtime {name}."))

    lint_text = subparsers.add_parser("lint-text", help="Run the runtime voice lint.")
    lint_text.add_argument("file", type=Path)
    lint_text.add_argument("--profile", choices=("consulting", "longform"), required=True)
    workspace_arg(lint_text)

    lint_deck = subparsers.add_parser("lint-deck", help="Lint a deck JSON or YAML specification.")
    lint_deck.add_argument("deck", type=Path)
    workspace_arg(lint_deck)

    generate = subparsers.add_parser("generate", help="Generate a PPTX and enforce the hard runtime gate.")
    generate.add_argument("deck", type=Path)
    generate.add_argument("output", type=Path)
    generate.add_argument("--template", type=Path)
    workspace_arg(generate)

    test = subparsers.add_parser("test-runtime", help="Run the bundled runtime test suite.")
    test.add_argument("--pytest-arg", action="append", default=[])
    workspace_arg(test)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = runtime_root(args.workspace)
        if args.command == "preflight":
            print(f"RUNTIME OK v{RUNTIME_VERSION} src={root / 'src'}")
            return 0
        if args.command == "info":
            print(json.dumps({
                "version": RUNTIME_VERSION,
                "archive": str(RUNTIME_ARCHIVE),
                "archive_sha256": RUNTIME_SHA256,
                "runtime_root": str(root),
                "template": str(root / "ow_default.pptx"),
                "python": sys.executable,
            }, indent=2))
            return 0
        if args.command in {"list-intents", "list-capabilities", "list-voice"}:
            return run_runtime(root, "--" + args.command)
        if args.command == "lint-text":
            return run_runtime(root, "--lint-text", str(args.file.resolve()), "--profile", args.profile)
        if args.command == "lint-deck":
            return run_runtime(root, "--lint-deck", str(args.deck.resolve()))
        if args.command == "test-runtime":
            env = os.environ.copy()
            env["PYTHONPATH"] = str(root / "src") + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
            command = [sys.executable, "-m", "pytest", "tests", "-q", "--color=no", *args.pytest_arg]
            return subprocess.run(command, cwd=root, env=env, check=False).returncode
        if args.command == "generate":
            deck = args.deck.resolve()
            output = args.output.resolve()
            template = args.template.resolve() if args.template else root / "ow_default.pptx"
            if not deck.is_file():
                raise AdapterError(f"Deck specification not found: {deck}")
            if not template.is_file():
                raise AdapterError(f"Template not found: {template}")
            output.parent.mkdir(parents=True, exist_ok=True)
            code = run_runtime(root, "--template", str(template), "--deck", str(deck), "--output", str(output))
            if code:
                return code
            result = read_gate(output)
            if not result["passed"]:
                print(json.dumps(result, indent=2), file=sys.stderr)
                print("GATE FAILED: fix the deck specification and rebuild; do not deliver this PPTX.", file=sys.stderr)
                return 3
            print(f"GATE PASSED: {output.parent / 'gate_result.json'}")
            return 0
        raise AdapterError(f"Unknown command: {args.command}")
    except AdapterError as exc:
        print(f"deck-builder: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
