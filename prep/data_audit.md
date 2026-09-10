# Data audit — inherited 2025 exercise data

Verified with `gdalinfo` on 2026-09-09 against
`malawi workshop 2025/activity sessions/QGIS Activity/`.

## Confirmed: three different CRSs in one exercise

| Layer | Declared CRS | Origin (E, N) | Pixel |
|---|---|---|---|
| `Nsanje_Landsat8_*` (all 4) | **UTM 36N** (EPSG:32636) | 724875, **−1856955** | 30 m |
| `Nsanje_Sentinel2_*` (both) | **UTM 36S** (EPSG:32736) | 724890, **8143030** | 10 m |
| `nsanje_buildings.shp` | **Web Mercator** (EPSG:3857) | — | vector |

**The Landsat files are the problem.** They declare UTM zone 36**N** but carry *negative*
northings (−1,856,955). Nsanje is in the southern hemisphere, so the correct encoding is zone
36**S** with a false northing of 10,000,000 — which is exactly what the Sentinel-2 files do
(10,000,000 − 1,856,955 ≈ 8,143,030, the same place).

Both resolve to the same ground location (upper left 35°06'35"E, 16°47'06"S in both), so QGIS
renders them correctly and the 2025 exercise worked. But:

- Anyone who reads the coordinate box sees a negative northing, which they should never be taught to
  accept.
- The layers do not share a CRS with each other or with the buildings, so every layer is being
  reprojected on the fly. That is silent until something goes wrong, and then it is baffling to
  a beginner.

**Action:** reproject everything to **EPSG:32736 (WGS 84 / UTM zone 36S)** before it goes on a
flash drive, and set that as the project CRS in every shipped `.qgz`. Extents match to within a
half pixel, so this is a clean warp.

## Unresolved: the Sentinel-2 acquisition date

**None of the six GeoTIFFs carry embedded date metadata.** The only metadata present is
`AREA_OR_POINT=Area`. There is no `TIFFTAG_DATETIME`, no acquisition tag, nothing.

So the discrepancy — filenames say **2023-03-16**, the 2025 slides describe March **2025**
imagery — **cannot be settled from the files.** The filename is the only assertion either way,
and filenames are not evidence.

**Action:** re-source the Sentinel-2 scene from Copernicus with the date confirmed at download. This matters because Day 1 Stage C hinges on showing participants
*the cloud-obscured scene from the day the flood peaked* — if we show them a scene from a
different year while saying that, the whole discussion collapses. Ties into Prabhmeet's
Sentinel-1 sourcing task; do both in one pass.

## Inventory (for flash drive planning)

| File | Size | Dimensions | Bands |
|---|---|---|---|
| `Nsanje_Landsat8_NIR_preflood.tif` | 2.3M | 1008 × 1008 @ 30 m | 1 |
| `Nsanje_Landsat8_NIR_postflood.tif` | 2.5M | 1008 × 1008 @ 30 m | 1 |
| `Nsanje_Landsat8_RGB_preflood.tif` | 6.4M | 1008 × 1008 @ 30 m | 3 |
| `Nsanje_Landsat8_RGB_postflood.tif` | 6.3M | 1008 × 1008 @ 30 m | 3 |
| `Nsanje_Sentinel2_NIR_20230316.tif` | 19M | 3022 × 3023 @ 10 m | 1 |
| `Nsanje_Sentinel2_RGB_20230316.tif` | 50M | 3022 × 3023 @ 10 m | 3 |
| `nsanje_buildings.*` | 12M | 36,077 polygons | Open Buildings |

Total ~98 MB. Trivial next to the QGIS installers (~1.5 GB per platform), so drive sizing is
driven by the installers. Adding Sentinel-1 SAR scenes will not change that.

Study area: Nsanje District, ~35°06'E–35°24'E, 16°47'S–17°03'S, roughly 30 × 30 km.

## Raster statistics (confirms the exercise works)

From `gdalinfo -hist` on the shipped rasters, 1,016,064 pixels each.

| | `NIR_preflood` | `NIR_postflood` |
|---|---|---|
| Value range | 7037 – 25850 | 6702 – 45034 |
| Below 10000 (the exercise's water threshold) | 0.95% | 2.97% |
| Mean / stddev | 15402 / 2089 | 19660 / 4245 |

Water pixels roughly triple between the two dates, so the `< 10000` threshold produces a visible,
teachable flood extent. The threshold inherited from 2025 is sound.

One note for whoever writes Stage C: **no flood peak date appears anywhere in the 2025 materials
or in the file metadata.** Stage C is framed as a hypothetical, which needs no such date — don't
introduce one.
