"""
Integration layer between JuniorSwarm / JuniorCraft and existing JuniorOmega components.

This shows how the new BitNet creative tooling can be called from omega_orchestrator.py
or use components from the spatial/ folder.
"""

from junioromega_bitnet_craft.juniorswarm.orchestrator import JuniorSwarmOrchestrator
from junioromega_bitnet_craft.juniorcraft.world_builder import JuniorCraftWorldBuilder


def integrate_with_omega_orchestrator(omega_state: dict) -> dict:
    """Example integration point."""
    swarm = JuniorSwarmOrchestrator()
    craft = JuniorCraftWorldBuilder()

    # Example: Use JuniorSwarm for agent coordination on top of Omega state
    swarm.register_agent("spatial_agent", "spatial_reasoner")
    result = swarm.coordinate(goal="Build coherent spatial structure", context=str(omega_state))

    return {
        "swarm_result": result,
        "message": "JuniorSwarm/JuniorCraft integrated with existing Omega orchestrator"
    }