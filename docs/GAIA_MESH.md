# Gaia terrain ingest

JuniorLLM `ports/gaia_terrain.py` writes a real quad mesh OBJ (`gaia_terrain_N.obj`).
Home agent: `scripts/gaia_terrain_prod.py --n=32 gaia terrain`.
This repo can import that OBJ in `blender/` later. No stub sphere.
UE5: JSON port only (`gaia_ue5.json`). Launch stays false unless operator sets JUNIOR_UE5=1 on a box that already has Unreal.
