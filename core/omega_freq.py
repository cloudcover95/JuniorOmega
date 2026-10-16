"""Angular frequency helpers for JuniorOmega.

Converts between Hz, rad/s (ω), and period. Pure math; no I/O.
"""

from __future__ import annotations

import math
from typing import Union

Number = Union[int, float]


def omega_from_hz(frequency_hz: Number) -> float:
    """Return angular frequency ω in rad/s from frequency in Hz."""
    f = float(frequency_hz)
    if f < 0:
        raise ValueError("frequency_hz must be non-negative")
    return 2.0 * math.pi * f


def period_from_omega(omega: Number) -> float:
    """Return period T in seconds from angular frequency ω (rad/s)."""
    w = float(omega)
    if w <= 0:
        raise ValueError("omega must be positive")
    return 2.0 * math.pi / w


def hz_from_omega(omega: Number) -> float:
    """Return frequency in Hz from angular frequency ω (rad/s)."""
    w = float(omega)
    if w < 0:
        raise ValueError("omega must be non-negative")
    return w / (2.0 * math.pi)


def omega_from_period(period_s: Number) -> float:
    """Return angular frequency ω in rad/s from period in seconds."""
    t = float(period_s)
    if t <= 0:
        raise ValueError("period_s must be positive")
    return 2.0 * math.pi / t


if __name__ == "__main__":
    # Self-check: 1 Hz -> 2π rad/s; period of 2π is 1 s; round-trip Hz.
    w = omega_from_hz(1.0)
    assert abs(w - 2.0 * math.pi) < 1e-12
    assert abs(period_from_omega(w) - 1.0) < 1e-12
    assert abs(hz_from_omega(w) - 1.0) < 1e-12
    assert abs(omega_from_period(1.0) - w) < 1e-12
    print("omega_freq self-check ok")
