"""Sign-off fields a pilot model must fill."""
from __future__ import annotations

from dataclasses import dataclass, field

REQUIRED = (
    "units",
    "title",
    "revision",
    "layer_map",
    "view_links",
    "dim_ok",
    "redline_log",
    "intent_flags",
)


@dataclass
class DrawingMeta:
    source: str
    kind: str  # scan|pdf|dxf|dwg|unknown
    units: str = "unknown"
    title: str = ""
    revision: str = ""
    layer_map: dict[str, str] = field(default_factory=dict)
    view_links: list[str] = field(default_factory=list)
    dim_ok: bool = False
    missing_elev: bool = False
    redline_log: list[str] = field(default_factory=list)
    intent_flags: list[str] = field(default_factory=list)
    holes: list[str] = field(default_factory=list)
    filled: dict[str, str] = field(default_factory=dict)
    filled_are_hypotheses: bool = True
