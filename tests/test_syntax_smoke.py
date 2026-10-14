"""Stdlib smoke test: every tracked Python file must at least compile.

Catches syntax errors across the repo without importing optional deps
(grpc, torch, bpy, etc.). Run: python3 -m unittest tests.test_syntax_smoke
"""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _python_files():
    try:
        out = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        return [ROOT / p for p in out.split()]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*.py") if ".git" not in p.parts]


class SyntaxSmokeTest(unittest.TestCase):
    def test_all_python_compiles(self):
        files = _python_files()
        self.assertTrue(files, "no Python files found")
        failures = []
        for p in files:
            try:
                compile(p.read_text(encoding="utf-8"), str(p), "exec")
            except (SyntaxError, UnicodeDecodeError) as e:
                failures.append(f"{p.relative_to(ROOT)}: {e}")
        self.assertFalse(failures, "\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
