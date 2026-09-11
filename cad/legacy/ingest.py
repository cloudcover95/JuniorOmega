"""Classify a file. No vendor OCR. Text sidecars only unless DXF ASCII."""
from __future__ import annotations

from pathlib import Path

from cad.legacy.schema import DrawingMeta

KINDS = {
    ".dxf": "dxf",
    ".dwg": "dwg",
    ".pdf": "pdf",
    ".png": "scan",
    ".jpg": "scan",
    ".jpeg": "scan",
    ".tif": "scan",
    ".tiff": "scan",
}


def classify(path: Path) -> DrawingMeta:
    path = Path(path)
    kind = KINDS.get(path.suffix.lower(), "unknown")
    meta = DrawingMeta(source=str(path), kind=kind)
    if kind == "dwg":
        meta.intent_flags.append("dwg_needs_dxf_export")
        meta.holes.append("native_dwg_not_parsed")
    if kind == "scan":
        meta.holes.append("raster_needs_vectorize")
        meta.intent_flags.append("source_quality_unknown")
    if kind == "pdf":
        meta.holes.append("pdf_may_be_raster_or_vector")
    return meta
