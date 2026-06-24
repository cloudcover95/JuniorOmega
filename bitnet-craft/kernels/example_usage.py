"""
Example usage and simple benchmarks for the kernels module.

Run this to test backend selection and basic simulation steps.
"""

from junioromega_bitnet_craft.kernels.simulation import create_simulation_kernels
from junioromega_bitnet_craft.kernels.backend import get_best_backend

import time

def main():
    print("=== Kernel Backend Demo ===")
    backend = get_best_backend()
    print(f"Selected backend: {backend.name}")

    kernels = create_simulation_kernels()

    # Simple benchmark: parallel agent steps
    class DummyAgent:
        def __init__(self, i): self.id = i
        def step(self): return f"agent_{self.id}_done"

    agents = [DummyAgent(i) for i in range(100)]

    start = time.time()
    results = kernels.parallel_agent_step(agents, lambda a: a.step())
    elapsed = time.time() - start

    print(f"Processed {len(agents)} agents in {elapsed:.4f}s using {backend.name}")
    print(f"Sample result: {results[0]}")

if __name__ == "__main__":
    main()