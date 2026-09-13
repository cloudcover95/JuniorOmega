# Mech agents

Scan / CAD / Blender jobs on this tree are dispatched by
`JuniorHome/packs/junior_mech_agents`.

- snap_scan → sensors / OmniVisionNode.capture
- emit_glb → blender/metal_render.py
- export_step → cad/

SolidWorks is an interchange target. This repo does not host SW COM.
Ternary router scores intent only. G-code still comes from GCodeGenerator.
