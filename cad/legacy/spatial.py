"""Spatial 3D notes — local LLM hook + HEIGHT line."""
from __future__ import annotations

import re

from cad.legacy.schema import DrawingMeta


def apply_height(meta: DrawingMeta, text: str) -> float | None:
    m = re.search(r"HEIGHT\s*[:#]?\s*([0-9.]+)", text, re.I)
    if m:
        h = float(m.group(1))
        meta.filled["height"] = str(h)
        return h
    try:
        from adaptations.omega_cad.spatial import guess_height

        g = guess_height(text)
        if g is not None:
            meta.filled["height"] = f"guess:{g}"
            meta.intent_flags.append("height_from_llm")
            return g
    except Exception:
        pass
    return None
