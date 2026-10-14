"""Validate config/pipeline.toml parses and has sane required keys (stdlib only)."""
import pathlib
import tomllib
import unittest

CONFIG = pathlib.Path(__file__).resolve().parent.parent / "config" / "pipeline.toml"


class PipelineConfigTest(unittest.TestCase):
    def setUp(self):
        with CONFIG.open("rb") as fh:
            self.cfg = tomllib.load(fh)

    def test_required_sections(self):
        for section in ("hardware", "tolerances", "storage"):
            self.assertIn(section, self.cfg)

    def test_hardware_strings(self):
        for key in ("target", "compute", "framework"):
            self.assertIsInstance(self.cfg["hardware"].get(key), str)

    def test_tolerances_in_unit_range(self):
        for key in ("svd_curvature_max", "anomaly_threshold"):
            val = self.cfg["tolerances"].get(key)
            self.assertIsInstance(val, (int, float), key)
            self.assertGreater(val, 0, key)
            self.assertLessEqual(val, 1, key)

    def test_storage(self):
        self.assertIn(self.cfg["storage"].get("format"), {"parquet", "csv", "json", "arrow"})
        self.assertIsInstance(self.cfg["storage"].get("compression"), str)


if __name__ == "__main__":
    unittest.main()
