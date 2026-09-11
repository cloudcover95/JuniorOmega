"""Stdlib box mesh → OBJ + ASCII STL. No trimesh."""
from __future__ import annotations

from pathlib import Path


def box_verts(w: float, d: float, h: float) -> list[tuple[float, float, float]]:
    return [
        (0, 0, 0),
        (w, 0, 0),
        (w, d, 0),
        (0, d, 0),
        (0, 0, h),
        (w, 0, h),
        (w, d, h),
        (0, d, h),
    ]


FACES = (
    (0, 1, 2),
    (0, 2, 3),
    (4, 6, 5),
    (4, 7, 6),
    (0, 4, 5),
    (0, 5, 1),
    (1, 5, 6),
    (1, 6, 2),
    (2, 6, 7),
    (2, 7, 3),
    (3, 7, 4),
    (3, 4, 0),
)


def write_obj(path: Path, w: float, d: float, h: float) -> None:
    verts = box_verts(w, d, h)
    lines = ["# JuniorOmega legacy box", f"# volume {w*d*h}"]
    for x, y, z in verts:
        lines.append(f"v {x} {y} {z}")
    for a, b, c in FACES:
        lines.append(f"f {a+1} {b+1} {c+1}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_stl(path: Path, w: float, d: float, h: float) -> None:
    verts = box_verts(w, d, h)
    out = ["solid junior_legacy"]
    for a, b, c in FACES:
        out.append("  facet normal 0 0 0")
        out.append("    outer loop")
        for i in (a, b, c):
            x, y, z = verts[i]
            out.append(f"      vertex {x} {y} {z}")
        out.append("    endloop")
        out.append("  endfacet")
    out.append("endsolid junior_legacy")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
