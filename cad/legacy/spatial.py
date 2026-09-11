"""Spatial 3D notes — JuniorBitNetDraft if on path, else HEIGHT line."""
from __future__ import annotations

import re

from cad.legacy.schema import DrawingMeta


def apply_height(meta: DrawingMeta, text: str) -> float | None:
    m = re.search(r"HEIGHT\s*[:#]?\s*([0-9.]+)", text, re.I)
    if m:
        h = float(m.group(1))
        meta.filled["height"] = str(h)
        meta.filled["port"] = "sidecar-HEIGHT"
        return h
    try:
        from adaptations.omega_cad.draft import interpret

        call = interpret(text, meta.holes)
        meta.filled["port"] = call.port
        meta.filled["draft_rec"] = call.rec
        if call.height is not None:
            meta.filled["height"] = f"draft:{call.height}"
            meta.intent_flags.append("height_from_JuniorBitNetDraft")
            return call.height
        if not call.allow_extrude:
            meta.intent_flags.append("draft_blocked_extrude")
    except Exception:
        try:
            from adaptations.omega_cad.spatial import guess_height

            g = guess_height(text)
            if g is not None:
                meta.filled["height"] = f"guess:{g}"
                return g
        except Exception:
            pass
    return None
