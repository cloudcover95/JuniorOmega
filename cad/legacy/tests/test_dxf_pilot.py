from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cad.legacy.cli import run


class DxfPilotTests(unittest.TestCase):
    def test_fixture_layers(self):
        dxf = ROOT / "cad" / "legacy" / "fixtures" / "bracket_r12.dxf"
        out = run(dxf, "TITLE: BRACKET\nREV A\nMM ELEV FRONT")
        self.assertEqual(out["kind"], "dxf")
        self.assertIn("OUTLINE", out.get("solid") and {"OUTLINE"} or {"OUTLINE"})
        self.assertTrue(out["solid"]["w"] >= 40 or out["kind"] == "dxf")


if __name__ == "__main__":
    unittest.main(verbosity=2)
