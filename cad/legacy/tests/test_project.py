from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cad.legacy.project import export


class ProjectTests(unittest.TestCase):
    def test_writes_obj_stl_meta(self):
        dxf = ROOT / "cad" / "legacy" / "fixtures" / "bracket_r12.dxf"
        side = (ROOT / "cad" / "legacy" / "fixtures" / "bracket_r12.sidecar.txt").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory() as td:
            out = export(dxf, side, Path(td))
            names = set(out["files"])
            self.assertTrue({"meta.json", "model.obj", "model.stl", "layers.json"} <= names)
            self.assertEqual(out["solid"]["h"], 8.0)
            self.assertEqual(out["solid"]["volume"], 40.0 * 20.0 * 8.0)
            self.assertTrue(out["layers"]["layer_ok"])
            self.assertTrue((Path(td) / "model.obj").read_text().startswith("# JuniorOmega"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
