"""Fill missing title/units/rev from sidecar text. Hypotheses only."""
from __future__ import annotations

import re

from cad.legacy.schema import DrawingMeta


def fill_from_text(meta: DrawingMeta, text: str) -> DrawingMeta:
    t = text.upper()
    if meta.units == "unknown":
        if "MM" in t or "MILLI" in t:
            meta.filled["units"] = "mm"
            meta.units = "mm"
        elif "INCH" in t or "IN." in t:
            meta.filled["units"] = "inch"
            meta.units = "inch"
    m = re.search(r"REV(?:ISION)?\s*[:#]?\s*([A-Z0-9.-]+)", text, re.I)
    if m and not meta.revision:
        meta.revision = m.group(1)
        meta.filled["revision"] = meta.revision
    m = re.search(r"TITLE\s*[:#]?\s*(.+)", text, re.I)
    if m and not meta.title:
        meta.title = m.group(1).strip()[:80]
        meta.filled["title"] = meta.title
    if "ELEV" not in t and "SECTION" not in t:
        meta.missing_elev = True
        if "elevation" not in meta.holes:
            meta.holes.append("elevation")
    meta.filled_are_hypotheses = True
    try:
        from adaptations.omega_cad.fill import propose

        meta.filled.update(propose(meta.holes, text))
    except Exception:
        pass
    return meta
