"""Run pilot on a folder. Stop on first sheet that cannot release."""
from __future__ import annotations

import json
from pathlib import Path

from cad.legacy.cli import run

SHEETS = {".dxf", ".dwg", ".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def sidecar_for(path: Path) -> str:
    for name in (path.with_suffix(".sidecar.txt"), path.parent / f"{path.stem}.sidecar.txt"):
        if name.is_file():
            return name.read_text(encoding="utf-8")
    return ""


def batch(folder: Path) -> dict:
    folder = Path(folder)
    results = []
    for path in sorted(folder.iterdir()):
        if path.suffix.lower() not in SHEETS:
            continue
        out = run(path, sidecar_for(path))
        results.append(out)
        if not out["pilot"]["release_rest_of_archive"]:
            return {"stopped": path.name, "ok": False, "results": results}
    return {"stopped": None, "ok": True, "results": results}


def main(argv: list[str]) -> int:
    import sys

    folder = Path(argv[1]) if len(argv) > 1 else Path("cad/legacy/fixtures")
    report = batch(folder)
    print(json.dumps(report, indent=2, default=str))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv))
