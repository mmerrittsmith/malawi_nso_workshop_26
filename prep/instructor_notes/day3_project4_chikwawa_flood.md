# Project 4 — instructor notes (not for participants)

Answers checked 15 Sep 2026 by running the same steps with `qgis_process` in **QGIS 3.44.14** on
the files in `day3_projects/project4_chikwawa_flood/`.

## Expected numbers

| Step | Before flood (19 Sep 2024) | After flood (14 Mar 2025) |
|---|---|---|
| Pixels below 10,000 | 0.45% | 1.24% |
| Polygonize: all shapes | 761 | **1,666** |
| Filter `"DN" = 1` | 750 | **1,576** |
| Buildings (layer total) | 93,705 | 93,705 |
| Join, discard unjoined | 12 | **55** |

Both join types (one-to-many default, one-to-one) give the same count, so the default doesn't
double-count.

## Extension A — the cut-off matters a lot here

| Threshold (after flood) | Water pixels | Flooded buildings |
|---|---|---|
| < 9,000 | 0.43% | 12 |
| **< 10,000** | 1.24% | **55** |
| < 11,000 | 2.37% | 156 |

Unlike Nsanje, Chikwawa's histogram has **no clean dip at 10,000**. The dark pixels run in a flat
shoulder into the land hump, so a 10% change in the cut-off moves the answer from 12 to 156. This is
the best discussion in the project: the threshold is a judgment call with consequences, like a
poverty line. Steer people away from "which number is right" and toward "how would you report
this honestly" (a range, with the method stated).

## Extension B

12 buildings touch water in September, before any flood: mostly along the river channel. They're
not all inside the 55, so it's "roughly 55, some of which are always next to the river", not
"55 − 12 = 43".

## Common problems

- **Join returns 0 in a fraction of a second:** the water-shapes layer points at a file that isn't
  there (warning triangle in the Layers panel), often after opening a checkpoint saved with a bad
  path. Right-click ▸ Change Data Source… ▸ `outputs/water_postflood_shapes.geojson`.
- **"No spatial index exists for input layer" warning:** harmless. The buildings ship with a
  `.qix` index, so it shouldn't appear unless that file wasn't copied.
- **`"DN" == 1` gives a syntax error** on GeoJSON and shapefiles (OGR SQL) but works on GeoPackage. The handout
  uses `"DN" = 1`, which works on both. Day 1's slide 83 uses `==`. It works there only if the
  polygons are saved as GeoPackage.
- **Join returns all 93,705 buildings:** "Discard records which could not be joined" left
  unticked.
- **Join returns 0:** they joined to the unfiltered shapes and the filter was lost, or chose the
  wrong layer in "By comparing to". Check the feature count of the water layer is 1,576.
- **Raster Calculator expression invalid:** typed layer name without the `@1`, or curly quotes
  from copying out of a PDF. Double-click the band instead of typing it.
- **Coordinates show a different EPSG:** project CRS was set by a layer loaded from somewhere else.
  All project files are EPSG:32736.

## Why no radar

Sentinel-1 finds only 1–9% of the Landsat flood water in this square, versus about half in Nsanje,
probably because of marsh vegetation (Elephant Marsh) and water that had drained by the next pass.
The SAR extension stays a Day 1, Nsanje-only activity. Candidate radar files are in
`data_library/_raw/project4/` if that's worth revisiting.

## Data

See `prep/data_library.md` and `prep/scripts/build_project4_chikwawa.sh`.
