# Project 2 — instructor notes (not for participants)

Answers checked 16 Sep 2026 with `qgis_process` in **QGIS 3.44.14**, on the files in
`day3_projects/project2_zomba_urban_growth/`.

## Expected numbers

| Step | Answer |
|---|---|
| Built-up surface, 2015 | 11.16 km² |
| Built-up surface, 2020 | 12.62 km² (+13%) |
| Growth shapes at `> 500` m² per cell | **343** |
| Area those shapes cover | 6.04 km² |
| Buildings intersecting them (default join) | **5,669** |
| …unique buildings (one-to-one join) | 5,668 |
| Buildings in the square | 123,779 |

Per area (Part 5), built-up km²:

| Area | 2015 | 2020 | Growth | % |
|---|---|---|---|---|
| Zomba City | 4.53 | 4.75 | 0.22 | +5 |
| TA Mlumbe | 1.71 | 1.97 | 0.26 | +15 |
| TA Malemia | 1.69 | 1.95 | 0.26 | +15 |
| TA Chikowi | 1.34 | 1.64 | 0.30 | +22 |
| TA Mwambo | 1.14 | 1.47 | 0.32 | +28 |
| TA Kuntumanji | 0.74 | 0.83 | 0.09 | +12 |

**The point of the project:** the city has the most built-up land and the least growth. Everything is
happening in the traditional authorities around it. Push people toward what that means for a
boundary drawn decades ago, and for any statistic reported by city limits.

## Extension A — the cut-off

| Cut-off | Growth shapes | Buildings |
|---|---|---|
| > 200 m² | 650 | 14,889 |
| **> 500 m²** | **343** | **5,669** |
| > 1000 m² | 87 | 1,454 |

Ten times fewer buildings between the loosest and tightest choice. Same lesson as the flood
threshold on Day 1: the number depends on a decision somebody made, so report the decision.

## Extension C — growth per person

Population from WorldPop 2025 (`mwi_pop_2025_CN_100m_R2025A_v1.tif`, now in the project folder),
summed per area with Zonal statistics:

| Area | Growth (km²) | People 2025 | New built-up m² per person |
|---|---|---|---|
| TA Mwambo | 0.32 | 31,117 | **10.3** |
| TA Chikowi | 0.30 | 36,457 | **8.2** |
| TA Malemia | 0.26 | 44,094 | **5.9** |
| TA Mlumbe | 0.26 | 44,178 | **5.9** |
| TA Kuntumanji | 0.09 | 22,010 | **4.1** |
| Zomba City | 0.22 | 123,333 | **1.8** |

TA Mwambo gains about ten square meters of new building per resident; Zomba City under two. The
city has four times the people of any TA and the least new building, which is the same finding as
Part 5 from the other direction.

## Why not measure growth from the Sentinel-2 pictures

Both dates are dry season. A built-up index (SWIR vs NIR) marks **82% of the square as built-up in
2016 and 73% in 2026**, against a true share of about 3%, because dry bare soil reflects like a
roof. Of the pixels it calls "new built-up", about **1%** are built-up in the ESA land cover map.
If a participant asks why we didn't just difference the pictures, that's the answer, and it is
Part 2 of the handout.

## What the built-up layer is

JRC Global Human Settlement built-up surface, R2023A, 100 m, modelled from Landsat and a 2018
Sentinel-2 composite, epochs every five years. **2025 and 2030 exist but are projections**, which is
why this project stops at 2020. Licence CC BY 4.0. Say "modelled" out loud when showing it to a
statistics office.

## Date mismatch to expect a question about

Pictures are 2016 and 2026; measurements are 2015 and 2020. The observed built-up epochs stop at
2020, and the ten-year picture pair shows change far more clearly than a five-year one would. Say
so before someone notices.

## Checkpoints

`project2_checkpoint_1/2/3.qgz`, rebuilt with `prep/scripts/make_project2_checkpoints.py`. All
paths are relative and the intermediates live in `checkpoints/data/`, so they open from a copy of
the folder with no `outputs/`.
