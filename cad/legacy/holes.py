"""Fill missing title/units/rev/views/redlines from sidecar. Hypotheses unless DIM_OK."""
from __future__ import annotations

import re

from cad.legacy.schema import DrawingMeta


def fill_from_text(meta: DrawingMeta, text: str) -> DrawingMeta:
    t = text.upper()
    if meta.units == "unknown":
        if re.search(r"\bMM\b|MILLI", t):
            meta.units = "mm"
            meta.filled["units"] = "mm"
        elif re.search(r"INCH|\bIN\.\b", t):
            meta.units = "inch"
            meta.filled["units"] = "inch"
    m = re.search(r"REV(?:ISION)?\s*[:#]?\s*([A-Z0-9.-]+)", text, re.I)
    if m and not meta.revision:
        meta.revision = m.group(1)
        meta.filled["revision"] = meta.revision
    m = re.search(r"TITLE\s*[:#]?\s*(.+)", text, re.I)
    if m and not meta.title:
        meta.title = m.group(1).strip()[:80]
        meta.filled["title"] = meta.title
    m = re.search(r"VIEW(?:S| LINKS)?\s*[:#]?\s*(.+)", text, re.I)
    if m:
        meta.view_links = [x.strip().lower() for x in re.split(r"[,|/]", m.group(1)) if x.strip()]
        meta.filled["view_links"] = ",".join(meta.view_links)
    for line in text.splitlines():
        if line.upper().startswith("REDLINE"):
            meta.redline_log.append(line.split(":", 1)[-1].strip() or line.strip())
    if re.search(r"DIM[_ ]?OK\s*[:#]?\s*(YES|TRUE|1)", t):
        meta.dim_ok = True
        meta.filled["dim_ok"] = "yes"
    if "ELEV" not in t and "SECTION" not in t:
        meta.missing_elev = True
        if "elevation" not in meta.holes:
            meta.holes.append("elevation")
    else:
        meta.missing_elev = False
        meta.holes = [h for h in meta.holes if h != "elevation"]
    meta.filled_are_hypotheses = not meta.dim_ok
    try:
        from adaptations.omega_cad.fill import propose

        meta.filled.update(propose(meta.holes, text))
    except Exception:
        pass
    return meta
