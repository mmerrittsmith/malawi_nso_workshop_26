# Data audit — inherited 2025 exercise data

Verified with `gdalinfo` on 2026-09-09 against
`malawi workshop 2025/activity sessions/QGIS Activity/`.

## Fixed: three different CRSs in one exercise

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
flash drive, and set that as the project CRS in every shipped `.qgz`.

### Fixed 2026-09-13 in `day1_floods/activity/`

All seven layers are now EPSG:32736. The 2025 originals are untouched.

- **Landsat (4 files):** relabeled, not warped. UTM 36N and 36S differ only by the 10,000,000 m
  false northing, so the fix is `gdal_translate -a_srs EPSG:32736` with every northing shifted by
  +10,000,000 (origin now 724875, 8143045). No resampling: pixel checksums and lat/long corners
  are identical to the originals. Recompressed LZW → DEFLATE, so the files are ~30% smaller.
- **Sentinel-2 (2 files):** already EPSG:32736, left unchanged.
- **Buildings:** reprojected from Web Mercator with `ogr2ogr -t_srs EPSG:32736`. 36,077
  features before and after, attribute values identical, sampled centroids identical in
  lat/long. `.cpg` is now UTF-8 (was ISO-8859-1); the text field is plus codes, so nothing
  changes.

The `< 10000` threshold and every statistic below still hold, since no pixel value changed.

**Added the same day:** `gadm41_MWI_1.*` (GADM 4.1 admin-1, the 28 districts), copied unchanged
from `Berkeley/projects/malawi/gadm41_MWI_shp/` for Stage A steps 3–4. It stays in **EPSG:4326
on purpose**: once everything else is 32736, it's the only layer that gives Stage A step 6 a
layer CRS different from the project CRS. Admin-1 rather than admin-2, because GADM's Malawi
admin-2 is traditional authorities, not districts.

## Inventory (for flash drive planning)

| File | Size | Dimensions | Bands |
|---|---|---|---|
| `Nsanje_Landsat8_NIR_preflood.tif` | 1.6M | 1008 × 1008 @ 30 m | 1 |
| `Nsanje_Landsat8_NIR_postflood.tif` | 1.7M | 1008 × 1008 @ 30 m | 1 |
| `Nsanje_Landsat8_RGB_preflood.tif` | 4.3M | 1008 × 1008 @ 30 m | 3 |
| `Nsanje_Landsat8_RGB_postflood.tif` | 4.5M | 1008 × 1008 @ 30 m | 3 |
| `Nsanje_Sentinel2_NIR_20230316.tif` | 19M | 3022 × 3023 @ 10 m | 1 |
| `Nsanje_Sentinel2_RGB_20230316.tif` | 50M | 3022 × 3023 @ 10 m | 3 |
| `nsanje_buildings.*` | 12M | 36,077 polygons | Open Buildings |
| `Nsanje_Sentinel1_VV_dB_preflood.tif` | 27M | 3024 × 3024 @ 10 m | 1 |
| `Nsanje_Sentinel1_VV_dB_postflood.tif` | 28M | 3024 × 3024 @ 10 m | 1 |
| `gadm41_MWI_1.*` | 1.3M | 28 districts | GADM 4.1, EPSG:4326 |

**Sentinel-1 (added 14 Sep):** Sentinel-1A IW, relative orbit 6, from Microsoft Planetary Computer's
`sentinel-1-rtc` collection (already terrain-corrected, gamma0), VV band converted to dB and cut to
the Landsat grid exactly (same origin, 10 m pixels, EPSG:32736). Pre-flood 2024-09-07
(`S1A_IW_GRDH_1SDV_20240907T030843_…_06C7A2`), post-flood 2025-03-18
(`S1A_IW_GRDH_1SDV_20250318T030837_…_0736FC`). Threshold check in `agenda.md`, Stage C.

Total ~93 MB. Trivial next to the QGIS installers (~1.5 GB per platform), so drive sizing is
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
