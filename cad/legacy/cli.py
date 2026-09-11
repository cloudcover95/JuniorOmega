#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from cad.legacy.holes import fill_from_text
from cad.legacy.ingest import classify
from cad.legacy.layers import validate
from cad.legacy.pilot import checklist
from cad.legacy.recon import primitives_from_dxf_text, to_3d
from cad.legacy.spatial import apply_height

LAYER_MAP = {
    "0": "_ignore",
    "DEFPOINTS": "_ignore",
    "DIMS": "dims",
    "DIMENSIONS": "dims",
    "TEXT": "annot",
    "NOTES": "annot",
    "TITLE": "annot",
    "OBJECT": "profile",
    "PART": "profile",
    "OUTLINE": "profile",
    "HIDDEN": "hidden",
    "PHANTOM": "hidden",
    "CENTER": "center",
    "HATCH": "cut",
    "SECTION": "cut",
}


def run(path: Path, sidecar: str = "") -> dict:
    meta = classify(path)
    if sidecar:
        fill_from_text(meta, sidecar)
    text = path.read_text(encoding="utf-8", errors="ignore") if path.suffix.lower() == ".dxf" else sidecar
    prims = primitives_from_dxf_text(text) if text else []
    layers = {p.layer for p in prims}
    if layers:
        meta.layer_map = {x: LAYER_MAP.get(x.upper(), f"misc_{x.lower()}") for x in layers}
    lv = validate(meta.layer_map)
    if not lv["layer_ok"]:
        meta.holes.append("layers")
        meta.intent_flags.append("layer_validation_failed")
    height = apply_height(meta, sidecar or text)
    solid = to_3d(meta, prims, height)
    gate = checklist(meta)
    if not lv["layer_ok"]:
        gate["release_rest_of_archive"] = False
        gate["missing"] = list(gate["missing"]) + ["layer_ok"]
    return {
        "source": meta.source,
        "kind": meta.kind,
        "units": meta.units,
        "title": meta.title,
        "revision": meta.revision,
        "layer_map": meta.layer_map,
        "layers": lv,
        "solid": solid.__dict__,
        "filled": meta.filled,
        "pilot": gate,
    }


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "project":
        from cad.legacy.project import export

        sheet = Path(argv[2])
        side = Path(argv[3]).read_text(encoding="utf-8") if len(argv) > 3 else ""
        dest = Path(argv[4]) if len(argv) > 4 else Path("cad_out") / sheet.stem
        print(json.dumps(export(sheet, side, dest), indent=2))
        return 0
    if len(argv) < 2:
        print("usage: python -m cad.legacy <file> [sidecar] | project <file> [sidecar] [dest]")
        return 2
    side = Path(argv[2]).read_text(encoding="utf-8") if len(argv) > 2 else ""
    print(json.dumps(run(Path(argv[1]), side), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
