from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import uuid


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "distributions" / "ai-platform" / "deck-builder"
ADAPTER = SKILL / "scripts" / "runtime_adapter.py"


class PackageTests(unittest.TestCase):
    def test_exact_knowledge_files_are_lf_normalized(self) -> None:
        knowledge = SKILL / "references" / "original_knowledge"
        for path in knowledge.glob("*.md"):
            with self.subTest(path=path.name):
                self.assertNotIn(b"\r\n", path.read_bytes())

    def test_package_validator(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_package.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "valid")

    def test_adapter_preflight_and_info(self) -> None:
        scratch = ROOT / ".deck-builder-work"
        scratch.mkdir(exist_ok=True)
        directory = scratch / f"deck-builder-test-{uuid.uuid4().hex}"
        directory.mkdir()
        try:
            preflight = subprocess.run(
                [sys.executable, str(ADAPTER), "preflight", "--workspace", str(directory)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(preflight.returncode, 0, preflight.stdout + preflight.stderr)
            self.assertIn("RUNTIME OK v2.6.18", preflight.stdout)

            info = subprocess.run(
                [sys.executable, str(ADAPTER), "info", "--workspace", str(directory)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(info.returncode, 0, info.stdout + info.stderr)
            payload = json.loads(info.stdout)
            self.assertEqual(payload["version"], "2.6.18")
            self.assertTrue(Path(payload["template"]).is_file())
        finally:
            shutil.rmtree(directory, ignore_errors=True)

    def test_adapter_rejects_failed_gate(self) -> None:
        spec = importlib.util.spec_from_file_location("runtime_adapter", ADAPTER)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        scratch = ROOT / ".deck-builder-work"
        scratch.mkdir(exist_ok=True)
        directory = scratch / f"deck-builder-gate-{uuid.uuid4().hex}"
        directory.mkdir()
        try:
            output = Path(directory) / "deck.pptx"
            (output.parent / "gate_result.json").write_text('{"passed": false}', encoding="utf-8")
            self.assertFalse(module.read_gate(output)["passed"])
        finally:
            shutil.rmtree(directory, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
