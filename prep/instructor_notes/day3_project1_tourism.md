# Project 1 — instructor notes (not for participants)

**Status: draft, 15 Sep 2026.** The project folder isn't built yet (see *Data to build*), and the
handout hasn't been run in QGIS. The numbers below were measured in Python on the data library files
the folder will copy, with a 3 km circle around each stop and QGIS's zonal-statistics rule (a pixel
counts if its center is inside the circle). What's visible in the imagery was checked on Sentinel-2
views of each stop from the same dates. Re-check everything once the folder exists.

## The idea

There are no calculations. Participants load eleven layers once, then visit eight places and flip
through the same six layers in the same order. The stops are chosen so the layers **disagree** in
different ways:

| | **Lights grew** | **Lights didn't grow (by eye)** |
|---|---|---|
| **Buildings grew** | Senga Bay, Monkey Bay | Cape Maclear, Mangochi lakeshore, Nkhata Bay |
| **Buildings didn't grow** | Likoma | Nkhotakota, Liwonde (Mvuu): real tourism, no signal |

That grid is the answer to Part 5.1 and the core of the report-back. It is also Lecture 3's
conclusion, which participants reach on their own: satellites map infrastructure, not tourists.

## Answer key

3 km circle around each stop. Each night lights cell is about 460 × 460 m, so a circle holds about
130 cells, fewer where it covers the lake. "Lights sum" is what Extension A gives. Two different
pixel counts, because they answer different questions:

- **Lit cells** = cells above 0. This is the honest count, and the one the sums are built from.
- **Visible cells** = cells above 0.5, which is roughly what stands out on the 0–5 color scale from
  step 1.6. This is what a participant counts **by eye** during the tour, and it is the number the
  handout quotes at Cape Maclear.

Re-checked 16 Sep 2026 against the files in the project folder, two ways: `native:zonalstatisticsfb`
on `tour_stops.gpkg`, and the same circles in numpy. The sums agree to three digits.

| # | Stop | Lodges | Built-up 2021 (ha) | OSM buildings | Lit cells 2014 → 2021 | Visible cells | Lights sum 2014 → 2021 | People 2025 |
|---|---|---|---|---|---|---|---|---|
| 1 | Senga Bay | 12 | 156 | 2,160 | 51 → 74 | 14 → 36 | 19.7 → 47.1 (+140%) | 12,901 |
| 2 | Cape Maclear | 25 | 76 | 2,866 | 55 → 58 | 17 → 27 | 27.2 → 38.3 (+41%) | 5,132 |
| 3 | Likoma | 8 | 60 | 2,415 | **0 → 49** | 0 → 23 | 0 → 24.6 | 13,119 |
| 4 | Nkhotakota WR (Tongole) | 1 | 0.6 | 3 | 0 → 0 | 0 → 0 | 0 → 0 | 20 |
| 5 | Mangochi lakeshore | 6 | 306 | 8,837 | 97 → 98 | — | 100.6 → 127.3 (+27%) | 30,220 |
| 6 | Nkhata Bay | 21 | 64 | 1,613 | 82 → 85 | — | 51.3 → 73.9 (+44%) | 18,481 |
| 7 | Monkey Bay | 4 | 275 | 4,859 | 91 → 103 | — | 69.1 → 107.8 (+56%) | 19,444 |
| 8 | Liwonde NP (Mvuu) | 3 | 3.1 | 50 | 0 → 0 | 0 → 0 | 0 → 0 | 1,337 |

Counting rules, so a different answer means a different rule and not a mistake: **lodges** are
`accommodation` points within 3 km of the circle's center; **OSM buildings** are outlines that
*intersect* the circle, which is what select-by-location gives; **built-up** is ESA WorldCover
class 50; **people** is a zonal sum of WorldPop 2025.

"Lodges" counts OSM hotels, guesthouses, hostels, campsites, chalets and motels, both points and
building outlines (as points). Brightest single pixel at any stop is 5.1 (Monkey Bay, 2014), so the
0–5 color scale in step 1.6 covers every stop.

Stop centers (lat, lon) for the build: Senga Bay −13.708, 34.613 · Cape Maclear −14.026, 34.838 ·
Likoma −12.080, 34.720 · Tongole −12.911, 34.050 · Mangochi lakeshore −14.319, 35.143 ·
Nkhata Bay −11.608, 34.300 · Monkey Bay −14.081, 34.923 · Mvuu −14.850, 35.294.

## Stop by stop

**1 · Senga Bay — the layers agree.** Growth at the southern end of the circle, plus a large new
cleared area there that isn't in 2016. The only stop where the lit area clearly spreads. Use it as
the reference: "this is what growth looks like, if you believe the layers." Push on the question at
the end: new light could be lodges or homes.

**2 · Cape Maclear — buildings grow, lights hardly move.** The densification of Chembe along the
beach is the clearest before/after on the tour. The lit area is nearly flat (55 → 58 cells).
**Careful:** the light does get brighter in total (+41%), which participants who do Extension A will
find. By eye, on a 0–5 scale, most of these cells stay dim purple, so they won't see it. That's a
good moment rather than a problem: "by eye" and "by number" gave different answers, and Senga Bay's
+140% is still far larger. Don't claim "no change in lights".

The OSM outline of Lake Malawi National Park covers only about 8% of this circle, so the handout
doesn't send people to the park boundary here.

**3 · Likoma — lights from nothing.** Dark every year 2012–2020, lit in 2021 (49 cells, sum 24.6)
and 2022 (46 cells, sum 22.9). Buildings show modest infill over nine years, nothing that happens in one. The COVID point is
solid: 2020–21 were the worst tourism years there have been. **We have not confirmed why the lights
appeared** (a power supply change on the island is the obvious guess). Don't state a cause unless
someone checks. There's also a technical reason it looks like a switch: the `average_masked`
product sets faint background light to zero. A place that gets a little brighter can jump from 0 to
"lit" in one year instead of rising gradually.

**4 · Nkhotakota — tourism with no signal.** This is the site from the first plan. Nothing in any
layer: 0.6 ha built-up, 3 mapped buildings in the whole circle, no light, about 20 people. The lodge is not visible at 10 m.
The riverbed is visibly wider and paler in 2025, which is the only change; don't let it be read
as development. Zooming out shows the woodland/farmland contrast at the reserve edge: clear at 10 m
near Bua Camp, about 14 km east. **Confirm it's visible on the 30 m basemap when taking the
screenshot.** If a pair wants to go further: Bua Camp's circle catches about 240 OSM buildings and
46% tree cover. Those are the villages outside the boundary, not the camp.

**5 · Mangochi lakeshore — big numbers, but whose?** The most built-up land, buildings, people and
lit area of any stop, but the lit area doesn't grow. The airstrip near the top of the circle is
Club Makokola's. The resorts are a thin line on the beach, and the growth in the imagery is homes
inland. The question: what happens if you add all of this up and call it tourism?

**6–8 · Your turn.**
- **Nkhata Bay** is like Cape Maclear: 21 lodges, a modest amount of new building, lit area flat
  (82 → 85 cells).
- **Monkey Bay** is like Senga Bay by the numbers (lit area 91 → 103 cells), but only 4 lodges. It's a town
  and a port, so it's also a good "is this tourism?" case.
- **Mvuu** is like Nkhotakota: 3 lodges, no light, almost no built-up. The OSM park outline covers
  about 80% of its circle.

## Extension B — every year, not just two

What `lights_by_year_snippet.py` prints (lights sum in each 3 km circle). Checked against
`qgis_process`, which gives the same values.

| Stop | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Senga Bay | 30.1 | 24.2 | 19.7 | 24.6 | 22.7 | 32.3 | 38.1 | 39.2 | 42.3 | 47.1 | 40.0 |
| Cape Maclear | 28.2 | 33.2 | 27.2 | 28.6 | 18.2 | 30.0 | 32.4 | 24.0 | 33.6 | 38.3 | 31.6 |
| Likoma | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **24.6** | 22.9 |
| Nkhotakota WR | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Mangochi lakeshore | 113.3 | 99.2 | 100.6 | 94.4 | 73.6 | 96.4 | 94.0 | 91.2 | 132.8 | 127.3 | 106.6 |
| Nkhata Bay | 82.6 | 62.3 | 51.3 | 58.3 | 53.4 | 69.0 | 76.1 | 71.7 | 69.1 | 73.9 | 74.7 |
| Monkey Bay | 104.0 | 76.8 | 69.1 | 58.9 | 51.0 | 74.6 | 85.5 | 94.0 | 94.2 | 107.8 | 93.0 |
| Liwonde NP (Mvuu) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

**The answer to "which year did Likoma switch on?" is 2021**, and the year matters: 2020–21 were the
worst tourism years there have been. This is the table behind Lecture 3's Likoma figure.

Two things worth pointing out if nobody does: every stop **dips around 2016** and rises afterward,
which is a reason to compare stops with each other rather than read one line on its own; and
**2012 is the brightest year** at three stops, which is a product artifact (April–December only, and
an older processing setup), not a boom.

## Extension C — people per lodge

WorldPop 2025 zonal sum ÷ lodges, from the answer key table:

| Stop | People per lodge |
|---|---|
| Mangochi lakeshore | 5,037 |
| Monkey Bay | 4,861 |
| Likoma | 1,640 |
| Senga Bay | 1,075 |
| Nkhata Bay | 880 |
| Liwonde NP (Mvuu) | 446 |
| Cape Maclear | 205 |
| Nkhotakota WR (Tongole) | 20 |

**Mangochi lakeshore and Monkey Bay** come top, and neither is mainly a tourist place: they are
towns where a lot of people live and a few lodges happen to be. **Cape Maclear**, the most touristy
stop on the tour, comes second from bottom. The ratio is measuring "town or not", not tourism, which
is exactly the kind of number that gets published with the wrong label on it.

## Why these choices

- **2014 and 2021, not 2012 and 2022.** 2012 is April–December only; 2012–2013 use a different
  processing setup; 2022 is a different product version (V2.2, adds NOAA-20). 2014 and 2021 are the
  widest pair from one consistent version. See `prep/data_library.md`.
- **Everything brightens a bit.** Every lit stop's total rises 2014→2021 (+27% to +140%), so compare
  stops with each other, not with zero. Lit *area* is what participants can see, and it separates
  the stops much more cleanly.
- **Fixed 0–5 scale on both years** is the one symbology lesson. If each year auto-stretches, the
  flip shows changes that aren't there.
- **Two imagery files, not sixteen.** One file per year covering all eight stops means a single tick
  box flips the whole tour between 2016 and 2025.
- **OSM buildings clipped to the stops.** The national file is 1.1 GB and would freeze laptops.

## Timing and priority

Project time is roughly 2h45 (Blocks 2–3). Rough budget: Part 1 45 min · Part 2 + Stop 1 20 min ·
Stops 2–5 about 12 min each · Part 4 20 min · Part 5 15 min.

- **Must do:** Part 1 (or open `project1_start.qgz`), Stops 1–4, Part 5.1 grid. Stops 1–4 cover all
  four boxes.
- **Drop first:** Part 4, then Stop 5.
- Anyone slow in Part 1 should open the checkpoint after 45 minutes, not keep fighting symbology.

## Things to check in QGIS 3.44 before printing

- Paletted/Unique values: Shift-click then Ctrl-click to leave only class 50, and that the minus
  button removes a multi-row selection.
- **Transparency ▸ Additional no data value** is where the handout says, and `0` hides the background
  on the float32 night lights (they have no nodata value set).
- What the night lights look like on first load (handout says "a dark rectangle… light spots").
- **Magma** and **Blues** are in the default color ramp list.
- **Ctrl+J** zooms to selected rows from the attribute table.
- Zonal statistics (Extension A) gives the sums in the answer key.
- WorldCover draw time zoomed out to all of Malawi. The file has **no overviews**. Build them
  (`gdaladdo`) before copying to the drives, or it will be slow on every laptop.
- Confirm "Lilongwe and Blantyre bright yellow, small towns dim purple" at Max 5.

## Data to build (`day3_projects/project1_tourism/`)

A `prep/scripts/build_project1_tourism.sh` along the lines of the project 2 script:

| File | How |
|---|---|
| `tour_stops.gpkg` | 8 points above, buffered 3 km, fields `stop` (1–8) and `name`, in handout order |
| `Sentinel2_2016.tif`, `Sentinel2_2025.tif` | Sentinel-2 L2A (Planetary Computer), red/green/blue, 8 × 8 km around each stop, 10 m. The +1000 offset removed from 2025 scenes. **Pre-stretched to 8-bit with one fixed stretch for both years** so they look alike with no symbology work. Mosaiced into one file per year with nodata outside the squares, plus overviews. Checked scenes: **22 Aug 2016** for all stops; 2025: **6 Sep** (Likoma, Nkhata Bay), **16 Sep** (Senga Bay, Cape Maclear, Nkhotakota), **29 Sep** (Mangochi, Monkey Bay, Mvuu). All under 5% cloud. There is smoke haze over the hills in the 2016 Senga Bay and Cape Maclear scenes, but not over the towns. |
| `accommodation.gpkg` | OSM `pois` points + `pois_a` polygons as points, `fclass` in hotel, guesthouse, hostel, camp_site, chalet, motel. 734 features nationally. Keep `name`, `fclass`. |
| `osm_buildings_stops.gpkg` | OSM buildings inside the 8 circles (about 21,900) |
| `protected_areas.shp` | Copy of OSM `protected_areas_a`, de-duplicated on `osm_id` (several parks appear twice, once as `national_park` and once as `nature_reserve`) |
| Library copies | `malawi_s2_rgb_2021_30m.tif`, WorldCover (with overviews), night lights 2014 and 2021, WorldPop 2025 |
| `project1_start.qgz` | Checkpoint with Part 1 done |
| `scorecard.docx` | 8 rows × columns: lodges · new buildings 2016→2025 · built-up · lights 2014 · lights 2021 · lights changed? · "would a satellite alone say tourism?" · the 2 × 2 grid on the back |

The Extension B console snippet is written: `lights_by_year_snippet.py`, in the project folder. It
has two `CHANGE ME` paths at the top that need setting to wherever the drive is mounted — do that
once on the day and read the two lines out, or it will eat ten minutes. Project 5 reuses it
(`work_split.md`).

**`agenda.md` and `prep/checklist.md` still describe the old version of this project** ("nightlights
over time at lodge/resort locations… Tourism infrastructure map + a nightlights trend table"). The
deliverable is now the scorecard + one map, with the trend table as Extension B.

## Screenshots needed

1. Symbology, Paletted/Unique values, only class 50 left
2. Night lights symbology, Min 0 / Max 5 / Magma
3. Layers panel in the final order
4. Attribute table with one stop selected and the zoom button
5. Senga Bay, 2016 and 2025 side by side
6. Likoma, lights 2014 and 2021 side by side
7. Example exported map
