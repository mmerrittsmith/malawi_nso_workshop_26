# Data library for the flash drives

What's built, where it came from, and how to rebuild it. The files themselves live in
`data_library/` and `installers/`, both gitignored. Everything is in **EPSG:32736** (UTM 36S),
clipped to Malawi's bounding box plus ~0.1° (32.55–36.05 E, 17.25–9.25 S). Built 14 Sep 2026.

**Drive footprint so far: ~2.6 GB** (1.95 GB library + 561 MB installer + 149 MB Day 1 activity).
`data_library/_raw/` (7.9 GB) is download scratch and does **not** go on the drives.

## Contents

| Folder | File(s) | Source | Processing | Size |
|---|---|---|---|---|
| `installers/` | `QGIS-OSGeo4W-3.44.14-1.msi` | download.osgeo.org — current 3.44 LTR | none | 561 M |
| `boundaries/` | `gadm41_MWI_0…3.shp` | GADM 4.1 (local copy in `projects/malawi/`) | reprojected | 20 M |
| `osm/` | 20 Geofabrik layers: roads, POIs, places, buildings, landuse, water, waterways… | Geofabrik Malawi free shapefile extract, 14 Sep 2026 | reprojected | 1.4 G |
| `population/` | `mwi_pop_2025_CN_100m_R2025A_v1.tif` | WorldPop R2025A, 2025, constrained, 100 m | reprojected with **sum** resampling; national total 21.93 M before and after | 20 M |
| `landcover/` | `ESA_WorldCover_10m_2021_v200_MWI.tif` | ESA WorldCover 2021 v200, 10 m | mosaicked, clipped, reprojected (nearest) | 256 M |
| `elevation/` | `copernicus_dem_glo90_MWI.tif` | Copernicus DEM GLO-90 (AWS open data) | mosaicked, clipped, reprojected to 90 m (bilinear) | 128 M |
| `rainfall/chirps_monthly/` | `chirps-v3.0.YYYY.MM.tif`, Jan 2015 – Aug 2026 (140 files) | CHIRPS v3.0 monthly, Africa | clipped, reprojected to 5 km (nearest) | 6 M |
| `nightlights/` | `viirs_vnl_v21_{2012-04–12, 2013…2021}_average_masked_MWI.tif`, `viirs_vnl_v22_2022_…` | EOG annual VNL, `average_masked`; downloaded by hand (EOG allows only browser downloads on free accounts) | clipped, reprojected to 460 m (nearest) | 2 M |
| `ndvi/` | `mod13a3_ndvi_YYYY.MM_MWI.tif`, Jan 2015 – Jul 2026 (139 files) | NASA MOD13A3 v061 (MODIS Terra, monthly, 1 km), via AppEEARS | scaled to real NDVI (−1 to 1), cloudy/snow pixels (reliability 2–3) set to no data, reprojected to 1 km (nearest); outside Malawi's outline is no data | 53 M |
| `imagery/` | `malawi_s2_rgb_2021_30m.tif` | ESA WorldCover 2021 Sentinel-2 cloudless composite (RGBNIR) | red/green/blue read at 30 m, stretched 150–1800 → 8-bit, JPEG with mask and overviews | 128 M |

Day 1 data is separate, in `day1_floods/activity/` — see [`data_audit.md`](data_audit.md).

### Project-specific data (in `day3_projects/`)

| Folder | Contents | Notes |
|---|---|---|
| `project2_zomba_urban_growth/` | `Zomba_Sentinel2_{RGB,NIR,SWIR}_{20160730,20260720}.tif` — 20 × 20 km around Zomba City, 10 m | Sentinel-2 L2A via Planetary Computer, 0% cloud. Int16 reflectance × 10000. The +1000 offset in post-2022 scenes is **removed**, so both dates are directly comparable (mean red 903 vs 866). A few dark pixels go slightly negative after that. |
| `project4_chikwawa_flood/` | `Chikwawa_Landsat8_{NIR,RGB}_{preflood,postflood}.tif`, `chikwawa_buildings.shp` (93,705) | Same layout as Nsanje: 1008 × 1008 at 30 m on Landsat's own grid, Landsat 8 19 Sep 2024 / 14 Mar 2025, Open Buildings v3 tile 18d. Square chosen for the most new water (10 km²) and least cloud (0.6%). Stage D workflow in QGIS 3.44.14 gives **55 flooded buildings**. No Sentinel-1: radar found only 1–9% of the Landsat flood water here. |

Rebuild with `prep/scripts/build_project2_zomba.sh` and `prep/scripts/build_project4_chikwawa.sh`.

## Things to know when using these

- **Night lights change version in 2022.** 2012–2021 are VNL V2.1 (Suomi NPP); 2022 is V2.2 (Suomi
  NPP + NOAA-20). 2012 is April–December only. 2012–2013 also use a different processing
  configuration (`vcmcfg`) from 2014 onwards (`vcmslcfg`). Treat jumps at 2013→2014 and
  2021→2022 with suspicion. Units: nW/cm²/sr; background and fires already zeroed.
- **Population is counts per 100 m cell.** Sum it within areas; don't average it.
- **Land cover classes** are ESA WorldCover codes: 10 tree cover, 20 shrubland, 30 grassland,
  40 cropland, 50 built-up, 60 bare/sparse, 70 snow/ice, 80 water, 90 wetland, 95 mangroves,
  100 moss/lichen.
- **CHIRPS months** after August 2026 weren't published at build time.
- **NDVI has gaps in the rainy season.** Cloudy pixels are removed: about 18% of Malawi in
  January 2025 against ~2% in July. District averages still work; a single pixel's time series may
  have holes. Seasonal cycle checks out: 2024 peaks in March (0.65), bottoms out in October (0.31).
- **The RGB basemap is for looking at, not measuring.** It's a stretched, JPEG-compressed 8-bit
  picture of a 2021 composite.

## Licenses and attribution

| Data | License | Attribution |
|---|---|---|
| GADM | "Freely available for academic use and other non-commercial use. Redistribution or commercial use is not allowed without prior permission." ([gadm.org/license](https://gadm.org/license.html)) | GADM 4.1, gadm.org |
| OpenStreetMap | ODbL | © OpenStreetMap contributors (extract by Geofabrik) |
| WorldPop | CC BY 4.0 | WorldPop, University of Southampton |
| ESA WorldCover (map and S2 composite) | CC BY 4.0 | © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium |
| Copernicus DEM | Copernicus DEM license (free, attribution) | Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the European Union and ESA |
| CHIRPS | Public domain (copyright waived, registered with Creative Commons; [CHC](https://www.chc.ucsb.edu/data/chirps)) | Citation requested: Funk et al. (2015), Climate Hazards Center, UC Santa Barbara |
| NASA MOD13A3 | No restrictions on reuse (NASA open data) | Didan, K. (2021). MODIS/Terra Vegetation Indices Monthly L3 Global 1km SIN Grid V061. NASA LP DAAC |
| EOG VIIRS night lights | CC BY 4.0 | Earth Observation Group, Payne Institute; Elvidge et al. (2021), *Remote Sensing* 13(5):922 |

**GADM's license matters for the drives:** it allows non-commercial use but says the data may not
be redistributed without permission. Putting it on participants' USB keys is redistribution.
Either ask GADM, or ship NSO's own boundaries or geoBoundaries (CC BY) instead.

## Rebuilding

- `prep/scripts/fetch_data_library.sh` — installer, boundaries, OSM, population, land cover,
  elevation, rainfall
- `prep/scripts/fetch_malawi_rgb.sh` — RGB basemap
- `prep/scripts/process_viirs.sh` — night lights, from hand-downloaded files in
  `data_library/_raw/viirs/`
- `prep/scripts/process_ndvi.sh` — NDVI, from an AppEEARS area request (MOD13A3.061 NDVI +
  pixel reliability layers, Malawi outline, Jan 2015 on) downloaded into `data_library/_raw/ndvi/`

## Not built yet

- **Day 2 household CSV** — Prabhmeet
