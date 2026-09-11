"""Write a complete project folder: meta, layers, redlines, OBJ, STL."""
from __future__ import annotations

import json
from pathlib import Path

from cad.legacy.cli import run
from cad.legacy.layers import validate
from cad.legacy.mesh import write_obj, write_stl


def export(sheet: Path, sidecar: str, dest: Path) -> dict:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    report = run(sheet, sidecar)
    solid = report["solid"]
    h = solid.get("h") or 0.0
    vol = None
    if h:
        write_obj(dest / "model.obj", solid["w"], solid["d"], h)
        write_stl(dest / "model.stl", solid["w"], solid["d"], h)
        vol = solid["w"] * solid["d"] * h
        solid["volume"] = vol
        report["solid"] = solid
    layers = validate(report.get("layer_map") or {})
    report["layers"] = layers
    (dest / "meta.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (dest / "layers.json").write_text(json.dumps(report.get("layer_map"), indent=2), encoding="utf-8")
    (dest / "REDLINES.md").write_text(
        "# redlines\n\n" + "\n".join(f"- {x}" for x in (report.get("filled") or {}).values()) + "\n",
        encoding="utf-8",
    )
    report["project"] = str(dest)
    report["files"] = sorted(p.name for p in dest.iterdir())
    return report
