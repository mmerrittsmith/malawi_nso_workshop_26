# Work split — Malawi NSO workshop, Zomba, 5–7 Oct 2026

Prep is the main cost, so we'll try to split that 50:50. During exercises we'll both circulate regardless of who leads. 


Two things drive the workload this year:
- **Day 1 re-treads last year's topics deliberately** — that is a content decision, and most of
  the source material already exists. The pace is a separate question: assume nobody remembers
  anything from Blantyre 2025 and teach it from scratch.
- **Day 3 is a menu of five pre-scoped mini-projects**, each needing data on the drive and its
  own handout. This is the single largest new build.

---

## Merritt — structure, logistics, welfare, Day 3 framing

**Logistics and infrastructure**
- [ ] Overall agenda, timing, coordination with NSO
- [ ] Flash drive master image and duplication
- [ ] **`.qgz` checkpoint projects for every stage boundary, all three days**
- [ ] Reprojection pass: everything to EPSG:32736 (see `prep/data_audit.md`)

**Teaching materials**
- [ ] **Lecture 1, blocks 1–3** — why we care, how imagery works, raster vs vector plus
      ready-made datasets (Open Buildings, OSM, GHSL)
- [ ] **Day 1 Stage C** — facilitation plan for the "why would this fail?" discussion, plus the
      SAR projector demo script
- [ ] **Lecture 2, first half** — imagery → welfare. Lead with small-area estimation: they
      already know census-plus-survey, and this is that with imagery standing in for the census
- [ ] **Day 2 code demo** — pre-run notebook from `mwi_pmt/`, outputs saved, nothing live
- [ ] **Exercise 2 data prep** — district poverty/consumption estimates CSV + GADM prep
- [ ] **Exercise 2 Stage A handout** — join + choropleth
- [ ] **Lecture 3** — the triage framework, the tourism worked example, and a short walk-through
      of the data-sources handout. Deliberately the shortest lecture of the three: Day 3's value
      is project time and spillover buffer.
- [ ] **"Where to get imagery" written guide** — the thing that lets them keep working after we
      leave. Copernicus Browser, EarthExplorer, WorldPop, Geofabrik, Open Buildings, WorldCover,
      CHIRPS. Registration needed, file sizes, what's free.
- [ ] **Project scoping template** + report-back structure
- [ ] **Mini-project 1: Tourism infrastructure** — data + handout
- [ ] **Mini-project 3: Population and access** — data + handout

---

## Prabhmeet — the Day 1 exercise, flood teaching, cartography, three mini-projects

**Exercise 1 — the whole of Day 1 (biggest single job)**
- [ ] Orientation happens **inside the flood exercise** — they learn QGIS while loading the
      first flood raster. Last year's standalone Exercise 0 used OSM and Google
      Satellite XYZ tiles and **does not work offline**; it needs replacing outright.
- [ ] Four stages, each ending at a checkpoint: A (QGIS on the flood data) · B (NIR detection) ·
      C (discussion + SAR demo — Merritt leads, but the SAR data is yours) · D (spatial join)
- [ ] Paced for someone who has never opened GIS software
- [ ] Participant handout, rewritten from `Remote Sensing Handout.docx`

**Sentinel-1 SAR preparation**
- [ ] Source Sentinel-1 scenes covering the Nsanje flood, pre and post
- [ ] Subset to the Landsat footprint, terrain-correct, reproject to EPSG:32736
- [ ] **Verify a simple threshold cleanly separates water before the workshop.** If it doesn't,
      we need to know that in September, while there is still time to fix it.
- [ ] SAR is a **projector demo** on Day 1 — but ship the data and a written walkthrough anyway,
      so anyone can redo it later or during Day 3.
- [ ] Deck slides 71–73 ("Caveats: imagery availability", 14 March 2025) are a ready-made cloud
      exhibit — worth a look. Any convincingly cloudy scene works, since Stage C is a hypothetical.

**Teaching materials**
- [ ] **Lecture 1, blocks 4–6** — choosing a sensor (Landsat, S2, S1, VIIRS individually, then
      the trade-off table), the tool landscape, and how to see water (Nsanje framing, histograms,
      thresholds). **Block 6 is the most important part of the lecture** — get them reading a
      histogram and calling the threshold before QGIS opens. If the lecture runs long, compress
      blocks 1 and 5 to protect it.
- [ ] **Lecture 2, second half** — cartography, incl. the live three-classification demo
- [ ] **Exercise 2 Stage B handout** — classification + Print Layout composer

**Mini-projects**
- [ ] **2: Urban growth** — data + handout
- [ ] **4: Flooding in another district** — data + handout. Nearly free: it's the Day 1 workflow
      on new data. This is the safety net project for anyone who struggled on Day 1.
- [ ] **5: Agricultural seasonality** — data + handout, reusing the snippet from project 1

**Malawi data library for the drives**
- [ ] VIIRS nightlights annual composites · WorldPop · ESA WorldCover · Geofabrik OSM extract ·
      Open Buildings · SRTM or MERIT DEM · CHIRPS subset · MODIS/Sentinel-2 NDVI · Sentinel-2
      scenes for the named project areas · GADM levels 0–3
- [ ] All reprojected to EPSG:32736, all clipped to sensible extents

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
`malawi workshop 2025/2B - Introduction to Geospatial Data Analysis.pptx` unless noted.
Use the **16:9 version** (modified 9 Dec 2025); ignore the `(4_3)` twin.

| # | Problem | Where |
|---|---|---|
| 1 | Titled "VIIRS CHIRPS" — CHIRPS is not VIIRS | slides 28–29 |
| 2 | "Sentinel-2 SAR" — SAR is **Sentinel-1**. Matters more this year, since SAR is now taught in its own right | slides 24, 77, 78, 81 |
| 3 | Sentinel-2 files dated **2023-03-16**, slides describe March **2025**. **Verified unresolvable** — the files carry no embedded date metadata, so the scene must be re-sourced with the date confirmed at download | data vs slides |
| 4 | **Verified:** Landsat declares UTM 36N but carries *negative* northings (should be 36S), Sentinel-2 uses 36S, buildings are Web Mercator. Three CRSs, all reprojecting on the fly. See [`prep/data_audit.md`](prep/data_audit.md) | exercise data |
| 5 | Exercise 0 depends on XYZ tile basemaps — dead offline | slides 50–58 |
| 6 | Data distributed via `https://shorturl.at/apCQx`, now unarchived | slide 58, handout |
| 7 | **No `.qgz` project file existed anywhere.** Participants rebuilt from scratch every time | everywhere |
| 8 | **All timing estimates are roughly 3× too fast.** Ignore them | everywhere |
