"""2D primitives + volume. Missing elevation ≠ silent solid."""
from __future__ import annotations

from dataclasses import dataclass

from cad.legacy.schema import DrawingMeta


@dataclass
class Prim2D:
    x0: float
    y0: float
    x1: float
    y1: float
    layer: str = "0"


@dataclass
class Solid3D:
    kind: str
    w: float
    d: float
    h: float | None
    volume: float | None
    hypothesis: bool


def primitives_from_dxf_text(text: str) -> list[Prim2D]:
    lines = text.splitlines()
    out: list[Prim2D] = []
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip() == "LINE":
            vals = {}
            j = i + 1
            while j < len(lines) - 1 and lines[j].strip() not in {"LINE", "ENDSEC", "0"}:
                code = lines[j].strip()
                if code in {"10", "20", "11", "21", "8"} and j + 1 < len(lines):
                    vals[code] = lines[j + 1].strip()
                    j += 2
                    continue
                j += 1
            try:
                out.append(
                    Prim2D(
                        float(vals.get("10", 0)),
                        float(vals.get("20", 0)),
                        float(vals.get("11", 0)),
                        float(vals.get("21", 0)),
                        vals.get("8", "0"),
                    )
                )
            except ValueError:
                pass
            i = j
        else:
            i += 1
    return out


def bounds(prims: list[Prim2D]) -> tuple[float, float]:
    if not prims:
        return 1.0, 1.0
    xs = [p.x0 for p in prims] + [p.x1 for p in prims]
    ys = [p.y0 for p in prims] + [p.y1 for p in prims]
    return max(xs) - min(xs) or 1.0, max(ys) - min(ys) or 1.0


def to_3d(meta: DrawingMeta, prims: list[Prim2D], height: float | None = None) -> Solid3D:
    w, d = bounds(prims)
    if height is None and (meta.missing_elev or not prims):
        meta.intent_flags.append("height_is_hypothesis")
        if "elevation" not in meta.holes:
            meta.holes.append("elevation")
        return Solid3D("box", w, d, None, None, True)
    h = height if height is not None else min(w, d) * 0.25
    return Solid3D("box", w, d, h, w * d * h, False)
