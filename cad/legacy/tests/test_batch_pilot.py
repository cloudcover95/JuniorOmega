from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cad.legacy.batch import batch
from cad.legacy.cli import run


class BatchPilotTests(unittest.TestCase):
    def test_complete_sidecar_releases(self):
        dxf = ROOT / "cad" / "legacy" / "fixtures" / "bracket_r12.dxf"
        side = (ROOT / "cad" / "legacy" / "fixtures" / "bracket_r12.sidecar.txt").read_text(
            encoding="utf-8"
        )
        out = run(dxf, side)
        self.assertEqual(out["units"], "mm")
        self.assertEqual(out["title"], "BRACKET")
        self.assertTrue(out["pilot"]["release_rest_of_archive"], out["pilot"])

    def test_batch_fixtures_ok(self):
        report = batch(ROOT / "cad" / "legacy" / "fixtures")
        self.assertTrue(report["ok"], report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
