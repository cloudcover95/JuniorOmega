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
    compile_info = None
    try:
        from junior_bitnet.compile_sheet import compile_sheet

        compile_info = compile_sheet(sidecar)
        (dest / "ACTIONS.json").write_text(
            json.dumps([a.__dict__ for a in compile_info.actions], indent=2),
            encoding="utf-8",
        )
    except Exception:
        compile_info = None
    report = run(sheet, sidecar)
    solid = report["solid"]
    h = solid.get("h") or 0.0
    blocked = compile_info is not None and not compile_info.ready
    if h and not blocked:
        write_obj(dest / "model.obj", solid["w"], solid["d"], h)
        write_stl(dest / "model.stl", solid["w"], solid["d"], h)
        solid["volume"] = solid["w"] * solid["d"] * h
        report["solid"] = solid
    elif blocked:
        report["blocked"] = True
        report["plain"] = "Finish ACTIONS.json before the 3D files."
    layers = validate(report.get("layer_map") or {})
    report["layers"] = layers
    (dest / "meta.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    (dest / "layers.json").write_text(json.dumps(report.get("layer_map"), indent=2), encoding="utf-8")
    (dest / "REDLINES.md").write_text(
        "# redlines\n\n" + "\n".join(f"- {x}" for x in (report.get("filled") or {}).values()) + "\n",
        encoding="utf-8",
    )
    report["project"] = str(dest)
    report["files"] = sorted(p.name for p in dest.iterdir())
    return report
