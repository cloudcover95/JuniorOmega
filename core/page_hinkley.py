"""Page-Hinkley change detector for streaming sensor signals.

Detects a sustained upward shift in the mean of a stream. Pure stdlib,
no I/O, no network.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PageHinkley:
    delta: float = 0.005      # tolerated drift magnitude
    threshold: float = 50.0   # alarm level (lambda)
    alpha: float = 1.0        # forgetting factor in (0, 1]

    def __post_init__(self) -> None:
        if self.threshold <= 0:
            raise ValueError("threshold must be positive")
        if not 0 < self.alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self.reset()

    def reset(self) -> None:
        self.n = 0
        self.mean = 0.0
        self.cum = 0.0
        self.cum_min = 0.0

    def update(self, x: float) -> bool:
        """Feed one sample; return True when a change is detected."""
        self.n += 1
        self.mean += (x - self.mean) / self.n
        self.cum = self.alpha * self.cum + (x - self.mean - self.delta)
        self.cum_min = min(self.cum_min, self.cum)
        return (self.cum - self.cum_min) > self.threshold


def _self_check() -> None:
    ph = PageHinkley(delta=0.005, threshold=20.0)
    assert not any(ph.update(1.0) for _ in range(200)), "false alarm"
    hit = None
    for i in range(200):
        if ph.update(5.0):
            hit = i
            break
    assert hit is not None, "shift not detected"
    ph.reset()
    assert ph.n == 0 and ph.cum == 0.0
    try:
        PageHinkley(threshold=0)
    except ValueError:
        pass
    else:
        raise AssertionError("bad threshold accepted")


if __name__ == "__main__":
    _self_check()
    print("page_hinkley self-check ok")
