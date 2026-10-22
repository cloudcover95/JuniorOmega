"""Spectral window functions for JuniorOmega (pure Python, additive module).

Provides Hann, Hamming, Blackman and rectangular windows plus helpers for
applying a window and computing its coherent gain and equivalent noise
bandwidth (ENBW). No third-party dependencies.
"""
import math

__all__ = ["window", "apply_window", "coherent_gain", "enbw"]


def window(name, n, periodic=False):
    """Return a list of n window coefficients.

    name: 'rect', 'hann', 'hamming' or 'blackman'.
    periodic=True gives the DFT-even form (denominator n instead of n-1).
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return [1.0]
    d = n if periodic else n - 1
    name = name.lower()
    if name == "rect":
        return [1.0] * n
    if name == "hann":
        return [0.5 - 0.5 * math.cos(2 * math.pi * k / d) for k in range(n)]
    if name == "hamming":
        return [0.54 - 0.46 * math.cos(2 * math.pi * k / d) for k in range(n)]
    if name == "blackman":
        return [0.42 - 0.5 * math.cos(2 * math.pi * k / d)
                + 0.08 * math.cos(4 * math.pi * k / d) for k in range(n)]
    raise ValueError("unknown window: %r" % name)


def apply_window(samples, name="hann", periodic=False):
    """Multiply samples element-wise by the named window."""
    w = window(name, len(samples), periodic)
    return [s * c for s, c in zip(samples, w)]


def coherent_gain(w):
    """Mean of the window coefficients (amplitude correction factor)."""
    if not w:
        raise ValueError("empty window")
    return sum(w) / len(w)


def enbw(w):
    """Equivalent noise bandwidth in bins: N * sum(w^2) / sum(w)^2."""
    s = sum(w)
    if s == 0:
        raise ValueError("window sums to zero")
    return len(w) * sum(c * c for c in w) / (s * s)


def _self_check():
    assert window("rect", 8) == [1.0] * 8
    h = window("hann", 9)
    assert abs(h[0]) < 1e-12 and abs(h[-1]) < 1e-12 and abs(h[4] - 1.0) < 1e-12
    for i in range(9):
        assert abs(h[i] - h[8 - i]) < 1e-12
    assert abs(window("hamming", 5)[0] - 0.08) < 1e-12
    assert abs(enbw(window("rect", 64)) - 1.0) < 1e-12
    assert abs(enbw(window("hann", 1024, periodic=True)) - 1.5) < 1e-9
    assert abs(coherent_gain(window("hann", 1024, periodic=True)) - 0.5) < 1e-9
    assert apply_window([2.0, 2.0, 2.0], "rect") == [2.0, 2.0, 2.0]
    assert window("blackman", 1) == [1.0]
    try:
        window("bogus", 4)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    return True


if __name__ == "__main__":
    print("omega_window self-check:", "OK" if _self_check() else "FAIL")
