"""Deterministic token-bucket rate limiter with an injectable clock.

Pure stdlib; no I/O, no network. Time is passed in explicitly so behavior
is reproducible in tests.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TokenBucket:
    capacity: float
    refill_rate: float  # tokens per second
    tokens: float = -1.0
    last_ts: float = 0.0

    def __post_init__(self) -> None:
        if self.capacity <= 0 or self.refill_rate < 0:
            raise ValueError("capacity must be > 0 and refill_rate >= 0")
        if self.tokens < 0:
            self.tokens = float(self.capacity)

    def _refill(self, now: float) -> None:
        if now < self.last_ts:
            raise ValueError("time went backwards")
        self.tokens = min(self.capacity, self.tokens + (now - self.last_ts) * self.refill_rate)
        self.last_ts = now

    def try_consume(self, now: float, cost: float = 1.0) -> bool:
        """Consume `cost` tokens at time `now`; return True if allowed."""
        if cost <= 0:
            raise ValueError("cost must be > 0")
        self._refill(now)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def wait_time(self, now: float, cost: float = 1.0) -> float:
        """Seconds until `cost` tokens are available (inf if never)."""
        self._refill(now)
        if self.tokens >= cost:
            return 0.0
        if self.refill_rate == 0:
            return float("inf")
        return (cost - self.tokens) / self.refill_rate


def _self_check() -> None:
    b = TokenBucket(capacity=2, refill_rate=1.0)
    assert b.try_consume(0.0) and b.try_consume(0.0)
    assert not b.try_consume(0.0)
    assert abs(b.wait_time(0.0) - 1.0) < 1e-9
    assert b.try_consume(1.0)
    assert not b.try_consume(1.0)
    assert b.try_consume(100.0) and b.try_consume(100.0) and not b.try_consume(100.0)
    try:
        b.try_consume(50.0)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


if __name__ == "__main__":
    _self_check()
    print("token_bucket self-check ok")
