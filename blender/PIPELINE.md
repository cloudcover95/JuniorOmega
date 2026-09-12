# JuniorCloud Blender host

Sits next to `metal_render.py`. Does not replace Metal / TDA shade.

```
python3 blender/jc_blender.py omega-lidar blender_out -1
python3 blender/jc_blender.py llm-fieldcore blender_out 0
python3 blender/jc_blender.py agi-capsule blender_out 1
blender --background --python blender/headless_worker.py -- blender_out/job.json
```

CI never requires Blender. Staged jobs write ASCII PLY + job.json.
JuniorCloud LLC.
