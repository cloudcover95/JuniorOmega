"""Validate mapped layers before a model is treated as a part."""
from __future__ import annotations

ALLOWED = {"_ignore", "dims", "annot", "profile", "hidden", "center", "cut"}


def validate(layer_map: dict[str, str]) -> dict:
    unknown = [k for k, v in layer_map.items() if v.startswith("misc_") or v not in ALLOWED]
    profiles = [k for k, v in layer_map.items() if v == "profile"]
    return {
        "layer_ok": bool(profiles) and not unknown,
        "profiles": profiles,
        "unknown": unknown,
    }
