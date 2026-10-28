"""Phase unwrapping helpers for angular-frequency signals (pure Python, additive).

unwrap(phases)        -> continuous phase sequence (removes 2*pi jumps)
inst_omega(phases, dt) -> instantaneous angular frequency estimates (rad/s)
"""
import math

TWO_PI = 2.0 * math.pi


def unwrap(phases, discont=math.pi):
    """Remove jumps larger than `discont` by adding multiples of 2*pi."""
    out = []
    offset = 0.0
    prev = None
    for p in phases:
        p = float(p)
        if prev is not None:
            d = p - prev
            if d > discont:
                offset -= TWO_PI * math.ceil((d - discont) / TWO_PI)
            elif d < -discont:
                offset += TWO_PI * math.ceil((-d - discont) / TWO_PI)
        out.append(p + offset)
        prev = p
    return out


def inst_omega(phases, dt):
    """Finite-difference angular frequency from (possibly wrapped) phases."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    u = unwrap(phases)
    return [(b - a) / dt for a, b in zip(u, u[1:])]


def _self_check():
    w, dt = 3.0, 0.1
    true = [w * i * dt for i in range(100)]
    wrapped = [math.atan2(math.sin(t), math.cos(t)) for t in true]
    u = unwrap(wrapped)
    assert all(abs((a - u[0]) - (b - true[0])) < 1e-9 for a, b in zip(u, true))
    om = inst_omega(wrapped, dt)
    assert all(abs(x - w) < 1e-9 for x in om)
    assert unwrap([]) == [] and inst_omega([0.0], dt) == []
    try:
        inst_omega([0.0, 1.0], 0)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    return True


if __name__ == "__main__":
    print("self-check ok" if _self_check() else "fail")
