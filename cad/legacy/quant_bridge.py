"""Optional absmean on drawing numbers. Engine is JuniorLLM."""
from __future__ import annotations


def profile_trits(values: list[float]) -> dict:
    try:
        from adaptations.omega_cad.quant import absmean, i2s_pack

        t, sc = absmean(values)
        return {"trits": t, "scale": sc, "packed": len(i2s_pack(t)), "port": "JuniorBitNetDraft"}
    except Exception:
        return {"trits": [], "port": None}
