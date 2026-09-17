# Pre-travel checklist

## Build

- [ ] **Pin one QGIS version** — current LTR is 3.44. Write every handout and screenshot with only
      that version and ship only that installer. 
- [ ] **Offline basemaps.** Ship the Nsanje Sentinel-2 RGB raster as the local imagery layer and
      GADM boundaries as vector reference.
- [ ] **`.qgz` checkpoints at every stage boundary.** Highest-value improvement over 2025, which
      shipped none. Given the pacing reality this is what stops one stuck person from stalling
      the room for an hour. **Built:** Day 1 stages A–D, project 1 (3) and project 4 (4).
      **Outstanding:** Day 2.
- [ ] **Handout granularity.** Every menu path spelled out, a screenshot per non-obvious dialog,
      and a "you should now see…" checkpoint after each step so people self-diagnose.
- [x] Reprojection pass on the Day 1 data: every raster and vector in `day1_floods/activity/` is
      now EPSG:32736 (see [`data_audit.md`](data_audit.md)). New data goes on in 32736 from the start.
      **One deliberate exception:** the GADM districts (`gadm41_MWI_1`) stay in lat/long
      (EPSG:4326), so Stage A step 6 has a layer whose CRS differs from the project's.

## Flash drives

- [ ] 10, 32 GB, exFAT. **Windows only** — every participant is bringing a Windows PC, so no
      macOS build is needed
- [ ] Contents:
  - QGIS Windows installer, 3.44 LTR, 64-bit. One installer, no alternatives
  - All exercise data, reprojected to EPSG:32736
  - All `.qgz` checkpoints
  - All handouts as PDF
  - All lecture slides as PDF
- [ ] **Leave handout sources off the drives.** Participants get the PDFs from `handouts/`; the
      `.Rmd` files and `screenshots/` folders inside each `day3_projects/` project stay behind.
      Ship each project's data, `checkpoints/` and an empty `outputs/`.
- [ ] **Right before imaging the drives:** delete `data_library/_raw/` (download scratch, ~8 GB,
      not for the drives). Not before — the build scripts reuse it.
- [ ] Test a drive end-to-end on a clean Windows machine
- [ ] Checksum-verify every drive after duplication; spot-check at least three on hardware
- [ ] **Check the installer isn't blocked by SmartScreen or antivirus when run from a USB drive.**
      This is the most likely way Day 1 morning goes wrong now that admin rights are settled.
      Know the click-through before you're standing over someone's machine.

## Verification

- [ ] Fresh-machine test: from a flash drive alone, on a clean Windows laptop with
      networking disabled, install QGIS and complete Days 1–2 plus at least two mini-projects start to finish.
      Run by someone who did not build the materials. This is a gold standard that we may not live up to since I don't 
      have a clean windows laptop, or a windows laptio in general.
- [ ] Run each exercise end to end at a slow pace
- [ ] Each handout followed literally by the *other* instructor, with no verbal help, to catch
      steps that only make sense to their author.
- [x] Confirm the SAR threshold actually separates water on the prepared rasters. **Checked 14
      Sep:** −16 dB works on the post-flood scene (81% agreement with the NIR mask); the pre-flood
      scene doesn't separate cleanly, so demo on post-flood only.
- [ ] Confirm Exercise 2's CSV joins cleanly to GADM — name spellings and key types are the
      usual failure point.
- [ ] Time each lecture aloud. Lecture 1 is a 3-into-1 compression and will want to run long.

## Day 3 mini-projects

Five pre-scoped, self-contained projects. Each needs its data on the drive, its own short handout, and a verified run-through. Participants choose at the end of Day 2.

- [ ] **1 · Tourism infrastructure** — nightlights over time at lodge/resort locations around
      Lake Malawi and Liwonde, plus OSM accommodation POIs and built-up change *(Merritt)*
- [x] **2 · Urban growth** — Zomba. Data, handout, checkpoints and answers done; needs screenshots and a run-through *(Prabhmeet)*
- [ ] **3 · Population and access** — people living >5 km from a health facility *(Prabhmeet)*
- [ ] **4 · Flooding in Chikwawa** — Day 1 workflow on the same March 2025 flood. Data built; expected answer 55 buildings *(Merritt)*
- [ ] **5 · Agricultural seasonality** — NDVI by district against CHIRPS rainfall *(Prabhmeet)*
- [ ] One-page scoping template, printed, one per participant
- [ ] Each project run end-to-end by the instructor who did *not* build it

## Malawi data library for the drives

Built so far, with sources and licenses: [`data_library.md`](data_library.md). Also built: a
Malawi-wide 30 m RGB basemap, and the QGIS 3.44.14 installer.

Needed so that Day 3 projects aren't dead ends. All reprojected to EPSG:32736, all clipped to
sensible extents.

- [x] VIIRS nightlights, annual composites (2012–2022)
- [x] WorldPop population raster (2025, 100 m)
- [x] ESA WorldCover land cover (2021, 10 m)
- [x] Geofabrik OSM extract (roads, health facilities, accommodation POIs)
- [ ] Google Open Buildings, national or several districts
- [x] DEM — Copernicus GLO-90 instead of SRTM/MERIT
- [x] CHIRPS precipitation subset (monthly, 2015 – Aug 2026)
- [x] NDVI series — MODIS MOD13A3 monthly, 1 km, Jan 2015 – Jul 2026
- [x] Sentinel-2 scenes for each named project area (Zomba, project 2)
- [x] GADM levels 0–3 — **check the license before shipping** (see `data_library.md`)
- [x] Landsat pair for the second flood district (Chikwawa, project 4). **No Sentinel-1:** radar finds only 1–9% of the Landsat flood water there, so the SAR extension stays Nsanje-only

## Laptops — participants bring their own

Settled: no laptops provided, everyone brings their own, all Windows PCs, and they can install
software. Sharing is acceptable if someone turns up without one.

That removes the two biggest risks we were carrying (no admin rights, and a mixed Windows/macOS
room). It replaces them with hardware we've never seen.

- [ ] **Send a pre-workshop email, and treat it as the single highest-value piece of prep.**
      Ask them to bring the laptop and its charger, to have roughly 10 GB free, to know their
      admin password, and — if they can — to install QGIS 3.44 before they arrive. Every person
      who arrives with QGIS already working is 20 minutes we get back on Day 1.
- [ ] Include the QGIS download link and a one-page install guide in that email
- [ ] Ask NSO to confirm how many participants own a laptop they can actually bring, so we know
      in advance how much pairing to plan for
- [ ] Bring a multi-port USB hub and a couple of spare USB sticks — with BYO machines, port
      availability and USB-C-only laptops are both live possibilities
- [ ] Power: 10 people with their own laptops means 10 chargers. Confirm outlet count with the
      venue and bring at least two power strips

**If people end up sharing**, put them in pairs and have them swap who is driving at each stage
boundary. Pair work is fine, and talking through the steps helps, but the person who never
touches the keyboard doesn't learn the software.

## Room kit

- [ ] Markers (the Day 1 goals board stays up all three days)
- [ ] Printed handouts, one set per participant
- [ ] Printed one-page scoping templates and mini-project handouts
- [ ] Two power strips, a USB hub, spare USB sticks
