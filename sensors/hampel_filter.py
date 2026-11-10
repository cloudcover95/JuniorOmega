"""Hampel despike filter (stdlib only, offline, no network, no serving).

Replaces samples that deviate from the rolling median by more than
k * 1.4826 * MAD with that median. Returns (filtered, flags).
"""
from __future__ import annotations

from statistics import median
from typing import List, Sequence, Tuple

MAD_SCALE = 1.4826


def hampel(x: Sequence[float], half_window: int = 3, k: float = 3.0) -> Tuple[List[float], List[bool]]:
    if half_window < 1:
        raise ValueError("half_window must be >= 1")
    n = len(x)
    out = list(map(float, x))
    flags = [False] * n
    for i in range(n):
        lo, hi = max(0, i - half_window), min(n, i + half_window + 1)
        w = [float(v) for v in x[lo:hi]]
        m = median(w)
        mad = median([abs(v - m) for v in w])
        if abs(float(x[i]) - m) > k * MAD_SCALE * mad and mad > 0:
            out[i] = m
            flags[i] = True
    return out, flags


def _selftest() -> None:
    clean = [1.0, 1.1, 0.9, 1.0, 1.05, 0.95, 1.0, 1.1, 0.9, 1.0]
    spiked = list(clean)
    spiked[5] = 50.0
    out, flags = hampel(spiked)
    assert flags[5] and abs(out[5] - 1.0) < 0.2, (out, flags)
    assert sum(flags) == 1, flags
    out2, flags2 = hampel(clean)
    assert not any(flags2) and out2 == clean
    assert hampel([])[0] == []
    try:
        hampel(clean, half_window=0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("hampel selftest ok")


if __name__ == "__main__":
    _selftest()
