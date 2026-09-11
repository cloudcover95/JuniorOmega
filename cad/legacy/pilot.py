"""Pilot gate — what one model must prove before the archive ships."""
from __future__ import annotations

from cad.legacy.schema import REQUIRED, DrawingMeta


def checklist(meta: DrawingMeta) -> dict:
    filled = {
        "units": meta.units != "unknown",
        "title": bool(meta.title),
        "revision": bool(meta.revision),
        "layer_map": bool(meta.layer_map),
        "view_links": bool(meta.view_links),
        "dim_ok": meta.dim_ok,
        "redline_log": bool(meta.redline_log),
        "intent_flags": True,
    }
    missing = [k for k in REQUIRED if not filled.get(k)]
    return {
        "release_rest_of_archive": not missing and not meta.holes,
        "missing": missing,
        "holes": list(meta.holes),
        "hypotheses": dict(meta.filled) if meta.filled_are_hypotheses else {},
    }
