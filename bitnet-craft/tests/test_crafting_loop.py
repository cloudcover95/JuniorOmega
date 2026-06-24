import pytest
from junioromega_bitnet_craft.juniorcraft.crafting_loop import JuniorCraftLoop

def test_crafting_loop_basic():
    loop = JuniorCraftLoop(theme="test_theme")
    loop.add_player("test_builder", role="builder")
    result = loop.step()
    assert result["tick"] == 1
    assert "actions" in result