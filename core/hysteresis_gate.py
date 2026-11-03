"""Hysteresis (Schmitt-trigger) gate for noisy scalar signals.

Pure-Python, no dependencies, no network. Additive module for JuniorOmega.

A gate turns ON when the signal rises to ``high`` and only turns OFF once it
falls to ``low`` (low < high), so jitter between the thresholds never causes
chatter. ``min_hold`` optionally requires a state to persist for that many
samples before a switch is allowed.
"""

from __future__ import annotations

from typing import Iterable, List


class HysteresisGate:
    def __init__(self, low: float, high: float, initial: bool = False, min_hold: int = 0) -> None:
        if not low < high:
            raise ValueError("low must be strictly less than high")
        if min_hold < 0:
            raise ValueError("min_hold must be >= 0")
        self.low = float(low)
        self.high = float(high)
        self.state = bool(initial)
        self.min_hold = int(min_hold)
        self._held = min_hold  # allow an immediate first switch

    def update(self, x: float) -> bool:
        """Feed one sample; return the gate state after it."""
        self._held += 1
        if self._held > self.min_hold:
            if not self.state and x >= self.high:
                self.state = True
                self._held = 0
            elif self.state and x <= self.low:
                self.state = False
                self._held = 0
        return self.state

    def run(self, xs: Iterable[float]) -> List[bool]:
        return [self.update(x) for x in xs]


def gate(xs: Iterable[float], low: float, high: float, initial: bool = False, min_hold: int = 0) -> List[bool]:
    """Convenience: gate a whole sequence with a fresh HysteresisGate."""
    return HysteresisGate(low, high, initial, min_hold).run(xs)


def edges(states: List[bool]) -> List[int]:
    """Indices where the gate state changed relative to the previous sample."""
    return [i for i in range(1, len(states)) if states[i] != states[i - 1]]


def _self_check() -> None:
    s = gate([0, 0.6, 0.4, 0.6, 1.0, 0.6, 0.4, 0.6, 0.1, 0.0], low=0.2, high=0.9)
    assert s == [False, False, False, False, True, True, True, True, False, False], s
    assert edges(s) == [4, 8]
    # chatter between thresholds never flips state
    assert gate([0.5, 0.3, 0.7, 0.3, 0.7], 0.2, 0.9) == [False] * 5
    # min_hold blocks a quick turn-off
    h = gate([1, 0, 0, 0], 0.2, 0.9, min_hold=2)
    assert h == [True, True, True, False], h
    try:
        HysteresisGate(1, 1)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


if __name__ == "__main__":
    _self_check()
    print("hysteresis_gate self-check OK")
