# Layer contract (agree before any batch)

Default map. Vendors who ignore this fail the pilot.

| Source layer | Junior name |
|--------------|-------------|
| 0, DEFPOINTS | `_ignore` |
| DIM*, DIMENSIONS | `dims` |
| TEXT*, NOTES, TITLE | `annot` |
| OBJECT, PART, OUTLINE | `profile` |
| HIDDEN, PHANTOM | `hidden` |
| CENTER | `center` |
| HATCH, SECTION | `cut` |

Anything else stays `misc_<original>` and is a redline, not a feature.
