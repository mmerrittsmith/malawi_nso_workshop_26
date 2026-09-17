# Work split — Malawi NSO workshop, Zomba, 5–7 Oct 2026

Prep is the main cost, so we'll try to split that 50:50. During exercises we'll both circulate regardless of who leads. 

The split is by day: **Merritt owns Day 1, Prabhmeet owns Day 2, and we split Day 3.** Owning a
day means its lectures, exercises, handouts, data and `.qgz` checkpoints.

| | Merritt | Prabhmeet |
|---|---|---|
| **Day 1** | Everything | — |
| **Day 2** | — | Everything |
| **Day 3** | Lecture 3 · data-sources guide · projects 1, 2 and 4 | Scoping template · projects 3 and 5 |
| **Logistics** | Agenda, NSO, flash drives | — |

**Where the Day 3 split ended up:** Merritt built projects 1, 2 and 4; Prabhmeet has 3 and 5 left,
plus the scoping template and all of Day 2. Project 2 moved across because its method needed
rebuilding from scratch (see its instructor notes).

Two things drive the workload this year:
- **Day 1 re-treads last year's topics deliberately** — that is a content decision, and most of
  the source material already exists. The pace is a separate question: assume nobody remembers
  anything from Blantyre 2025 and teach it from scratch.
- **Day 3 is a menu of five pre-scoped mini-projects**, each needing data on the drive and its
  own handout. This is the single largest new build.

---

## Merritt — Day 1, logistics, half of Day 3

**Logistics and infrastructure**
- [ ] Overall agenda, timing, coordination with NSO
- [ ] Flash drive master image and duplication
- [ ] **Load everything we need onto flash drives**
- [x] Reprojection pass on the inherited Day 1 data: everything to EPSG:32736 (see `prep/data_audit.md`)

**Day 1**
- [ ] **Lecture 1** — why we care, how imagery works, raster vs vector plus
      ready-made datasets (Open Buildings, OSM, GHSL), choosing a sensor, the tool landscape,
      how to see water
- [ ] **Exercise 1**
    - [ ] Orientation happens inside the flood exercise — they learn QGIS while loading the
      first flood raster. Last year's standalone Exercise 0 used OSM and Google
      Satellite XYZ tiles and does not work offline.
    - [x] Four stages, each ending at a `.qgz` checkpoint: A (QGIS on the flood data) · B (NIR
      detection) · C (discussion + SAR demo) · D (spatial join). Built in
      `day1_floods/checkpoints/`, rebuild with `prep/scripts/make_day1_checkpoints.py`
    - [ ] Paced for someone who has never opened GIS software
    - [ ] Participant handout **is the Exercise 1 slides**: PDF on the drive, plus a printed copy
      per participant so they aren't flipping windows on one laptop screen. Needs new Stage A
      slides, and every step at handout standard (menu path, screenshot, "you should now see…")
- [x] **Day 1 Stage C** — facilitation plan and SAR demo script:
      [`prep/instructor_notes/day1_stage_c.md`](prep/instructor_notes/day1_stage_c.md)

**Sentinel-1 SAR preparation**
- [x] Source Sentinel-1 scenes covering the Nsanje flood, pre and post: Sentinel-1A, 7 Sep 2024
      and 18 Mar 2025, same orbit track, already terrain-corrected (Planetary Computer)
- [x] Subset to the Landsat footprint, reproject to EPSG:32736 → `Nsanje_Sentinel1_VV_dB_*.tif`
- [x] **Verify a simple threshold separates water.** Works on the post-flood scene at −16 dB;
      not on the pre-flood scene (see Stage C in `agenda.md`)
- [ ] SAR is a **Day 1 extension**. Write the short walkthrough slides for it, so anyone can redo
      it later or during Day 3.
- [ ] Lecture Part B slides 67–69 ("Caveats: imagery availability", 14 March 2025) are a ready-made cloud
      exhibit. Any convincingly cloudy scene works, since Stage C is a hypothetical.

**Day 3**
- [ ] **Lecture 3** — the triage framework, the tourism worked example, and a short walk-through
      of the data-sources handout. The shortest lecture of the three.
- [x] **"Where to get imagery" written guide** — drafted:
      `day3_projects/data_sources/where_to_get_imagery.Rmd` → `handouts/where_to_get_imagery.pdf`.
      Eleven sources, what each needs, file sizes, and the traps (Sentinel-2's 2022 offset, EOG
      browser-only downloads, GHSL 2025 being a projection, the GADM licence). Doubles as the
      Lecture 3 block 3 walkthrough.
- [x] **Mini-project 1: Tourism infrastructure** — data, handout, 3 checkpoints, scorecard and the
      supplied console snippet. Screenshots done. **Project 5 reuses the snippet**
      (`day3_projects/project1_tourism/lights_by_year_snippet.py`), so hand it to Prabhmeet.
- [x] **Mini-project 2: Urban growth in Zomba** — taken over from Prabhmeet and finished: data,
      handout, 3 checkpoints, screenshots, instructor notes. 11.16 → 12.62 km² built-up,
      343 growth shapes, 5,669 buildings in them, growth fastest outside the city boundary.
- [x] **Mini-project 4: Flooding in Chikwawa** — data, handout, 4 checkpoints, instructor notes.
      Expected answer 55 buildings. The safety net for anyone who struggled on Day 1.
- [ ] **Left on all three:** a run-through by Prabhmeet (the instructor who didn't build them).

---

## Prabhmeet — Day 2, half of Day 3

**Day 2**
- [ ] **Lecture 2** — imagery → welfare. Lead with small-area estimation: they
      already know census-plus-survey, and this is that with imagery standing in for the census.
      Then cartography, incl. the live poverty-map demo and the three-classification comparison
- [ ] **Exercise 2 data prep** — household CSV (lat/long, household ID, consumption) + GADM
      district layer. Confirm it joins cleanly — name spellings and key types are the usual
      failure point
- [ ] **Post-stratified layer** — built in advance and shipped styled for the Stage B reveal.
      Participants don't compute weights in QGIS (see the prep note in `agenda.md`)
- [ ] **Exercise 2 Stage A handout** — households as points, then the coverage map
- [ ] **Exercise 2 Stage B handout** — district means, classification + Print Layout composer,
      then the reveal
- [ ] `.qgz` checkpoints at each Exercise 2 stage boundary
- [ ] **Day 2 code demo** — pre-run notebook from `mwi_pmt/`, outputs saved, nothing live.
      First thing cut if we're short on time

**Day 3**
- [ ] **Project scoping template** + report-back structure. Participants fill it in at the end
      of Day 2, so it sits with the Day 2 owner
- [ ] **Mini-project 3: Population and access** — data + handout. Nothing built yet; WorldPop and
      the OSM health facilities are already in the library
- [ ] **Mini-project 5: Agricultural seasonality** — data + handout. Nothing built yet; 139 months
      of NDVI, 140 of CHIRPS and the district boundaries are in the library. Reuses project 1's
      console snippet, with NDVI in place of night lights
- [ ] **Run through projects 1, 2 and 4**, which Merritt built

---

## Malawi data library for the drives

Whoever needs a layer sources it. All reprojected to EPSG:32736, all clipped to sensible extents.
The one exception is the Day 1 copy of the GADM districts, left in EPSG:4326 for Stage A step 6.

**Built 14–15 Sep, both halves** — see [`prep/data_library.md`](prep/data_library.md) for sources,
licenses and caveats:
- [x] GADM levels 0–3 (license question open) · Geofabrik OSM extract · VIIRS night lights
      2012–2022 · Copernicus DEM (instead of SRTM/MERIT) · Landsat pair for project 4 (Chikwawa;
      no Sentinel-1, the radar doesn't see that flood)
- [x] WorldPop 2025 · ESA WorldCover 2021 · Sentinel-2 for project 2 (Zomba, 2016 and 2026) ·
      CHIRPS monthly 2015–2026 · MODIS NDVI monthly 2015–2026
- [ ] Open Buildings beyond the Day 1 and project 4 areas — only if a project needs it

---

## Coding policy for handout authors

- **Expression fields: yes, throughout.** Day 1 already teaches two — the Raster Calculator
  (`Nsanje_Landsat8_NIR_preflood@1 < 10000`) in Stage B and the vector Filter (`"DN" == 1`) in
  Stage D, both inherited unchanged from the 2025 handout. Verified: those are the only two in
  the 2025 materials, and there is no Python anywhere in them. By Day 3 an expression box is
  familiar, so use Field Calculator and Select-by-expression freely.
- **Python console: one supplied snippet only.** It loops zonal statistics over a time series,
  for projects 1 and 5. Ten years of nightlights or a season of NDVI clicked through by hand is
  tedious and error-prone, which is the only reason it exists. Write it so the variables to
  change sit at the top with comments, and everything below is left alone.
- **Nobody is taught to program.** Label the snippet as a tool and say plainly in the handout
  that they are not expected to be able to write it.
- If you find yourself wanting the console anywhere else, raise it first — the aim is that a
  participant sees it once, in a controlled place.

---

## Fixes needed in the inherited 2025 materials

Both of us should know these before touching the decks. All in
`day1_floods/lectures/Day 1 Lecture Part B.pptx` unless noted. That deck is the working copy of the
2025 `2B - Introduction to Geospatial Data Analysis.pptx` (16:9 version). Slide numbers below are
from Merritt's edited version (92 slides, checked 13 Sep).

| # | Problem | Where |
|---|---|---|
| 1 | ~~Titled "VIIRS CHIRPS" — CHIRPS is not VIIRS~~ **Fixed 16 Sep** | — |
| 2 | ~~"Sentinel-2 SAR" — SAR is **Sentinel-1**~~ **Fixed 16 Sep**; the slides now say "Sentinel SAR". Worth making it "Sentinel-1" so people can find the data | slides 73, 74, 77 |
| 3 | ~~Landsat declares UTM 36N but carries *negative* northings (should be 36S), Sentinel-2 uses 36S, buildings are Web Mercator. Three CRSs, all reprojecting on the fly.~~ **Fixed 2026-09-13** — everything in `day1_floods/activity/` is now EPSG:32736. See [`prep/data_audit.md`](prep/data_audit.md) | exercise data |
| 4 | ~~Exercise 0 depends on XYZ tile basemaps — dead offline.~~ **Fixed 13 Sep** — Exercise 0 slides deleted; Stage A replaces it. (Caching the tiles for offline use was never an option: OSM's tile policy prohibits bulk and offline downloads, and Google's terms forbid caching.) | — |
| 5 | ~~Data distributed via a dead download link~~ **Fixed 16 Sep** — slide 51 now just lists the files | — |
| 6 | **No `.qgz` project file existed anywhere.** Participants rebuilt from scratch every time | everywhere |
| 7 | **All timing estimates are roughly 3× too fast.** Ignore them | everywhere |
