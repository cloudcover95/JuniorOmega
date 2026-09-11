from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cad.legacy.cli import run
from cad.legacy.pilot import checklist
from cad.legacy.schema import DrawingMeta


class LegacyTests(unittest.TestCase):
    def test_scan_fails_pilot(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sheet.png"
            p.write_bytes(b"\x89PNG")
            out = run(p, "TITLE: BRACKET\\nREV A\\nMM")
            self.assertEqual(out["kind"], "scan")
            self.assertFalse(out["pilot"]["release_rest_of_archive"])

    def test_checklist_blocks_holes(self):
        m = DrawingMeta("x.dxf", "dxf", holes=["elevation"])
        self.assertFalse(checklist(m)["release_rest_of_archive"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
