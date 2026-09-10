# Satellite Imagery for Measurement — Malawi NSO
**Zomba · 5–7 October 2026 · 3 days**

Instructors: Merritt Smith (UC Berkeley), Prabhmeet Kaur Matta (UC San Diego)
Participants: 5–10 expected, 15 maximum. Largely non-technical.
Tool: QGIS. **Fully offline** — all software and data distributed on flash drives.

| Day | Topic | Participants leave with |
|---|---|---|
| **1 · Mon 5 Oct** | QGIS + flood detection (Nsanje) | A CSV of flood-affected buildings |
| **2 · Tue 6 Oct** | Poverty mapping | An exported poverty map |
| **3 · Wed 7 Oct** | Their own project, from a menu of five | A finished project of their choosing |

---

## The day frame

All three days run **09:00 → 16:00**.

| | |
|---|---|
| 09:00 | **Block 1** |
| 10:30 | Tea |
| 10:45 | **Block 2** |
| 12:30 | Lunch |
| 13:30 | **Block 3** |
| 14:45 | Tea |
| 15:00 | **Block 4** |
| 16:00 | End |

---

## Design principles

**1. One exercise per day.** Last year we badly overestimated both participant ability and group
pace. All 2025 timing estimates should be ignored — the deck budgeted 45 minutes for the flood
exercise and 35 for the spatial join, and both are multiples of that in practice.

**2. Day 1 will re-hash last year's material, but teach it as if it was new.** Don't lie to them and tell them it's new, I just mean we shouldn't assume they remember anything. We want to establish
a common foundation and make sure everyone is starting from the same place on the exercises, since we don't know the composition of the room in advance this time. 

**3. Assume no internet.** 

**4. No participant coding.** In general, I think we can allow for some coding in QGIS in guided exercises, but we don't have time to teach them to code.

*What that means in practice:*
- **Expression fields are fair game throughout.** Day 1 already teaches two of them — the Raster
  Calculator (`Nsanje_Landsat8_NIR_preflood@1 < 10000`) in Stage B and the vector Filter
  (`"DN" == 1`) in Stage D, both inherited unchanged from the 2025 handout. By Day 3 an
  expression box is familiar ground, so Field Calculator and Select-by-expression can be used
  freely in the projects.
- **The Python console appears in exactly one place:** a supplied, ready-to-run snippet that
  loops zonal statistics over a time series. Projects 1 and 5 need it, because stepping through
  ten years of nightlights or a season of NDVI by hand through the GUI is tedious and
  error-prone. Participants run it and change one or two variables at the top. They do not write
  it, and nothing else in the workshop requires the console.
- **Nobody is taught to program.** The snippet is a labelled tool, and the handout says so.

**5. Everyone leaves with something they made.** Three artifacts, one per day.

---

## Day 1 — Monday 5 October
### QGIS and flood detection

| Block | Content |
|---|---|
| **1** | Welcome, introductions, **participant goals round** · Install QGIS from flash drive |
| **2** | **Lecture 1** — How imagery works, and how to see water |
| **3** | **Exercise 1** — Stages A and B |
| **4** | **Exercise 1** — Stages C and D · Wrap |

**Priority order**
- We would like to get them to the same place we got them to at the end of Satej's workshop last year, with a map of highlighted flood-affected buildings 
- Stage A can run lean or long depending on how the room handles the software.
- If short on time, the post-flood repetition in Stage B will be dropped first, picking up from the checkpoint
- If VERY short on time, we can shrink the SAR demo to just a brief walkthrough and overview
- If necessary, spill over to Day 2 morning

**Welcome.** Introductions, then a goals round: what do you want to learn, measure, understand, get out of this workshop?
We'll write them up, and try to direct them towards Day 3 project slection based on answers.

**Install — ideally start before the lecture.** Start installers early so installs can take place *during* the lecture by whichever instructor isn't speaking. 
Success criterion: QGIS opens on every machine by lunch.

Everyone brings their own Windows laptop and they can install software, so this should be
straightforward, but it's their hardware and we've never seen it. The likely problems are
SmartScreen or antivirus blocking the installer when it runs off a USB stick, someone not
knowing their admin password, and disk space. We'll have asked them by email beforehand to
install QGIS before they arrive, and anyone who managed it is twenty minutes we get back.

If someone turns up without a laptop they pair with someone else, and the two of them should
swap who is driving at each stage boundary so that both of them actually use the software.

### Lecture 1 — taught from scratch

| | Block | Lead |
|---|---|---|
| 1 | **Why we care** — three questions an NSO might ask: who was flooded, where is poverty concentrated, how is land use changing. We answer the first two this week. Blantyre poverty map and Nsanje flood imagery as anchors | Merritt |
| 2 | **How imagery works** — reflection off surfaces → sensor → bands → pixel grid + georeferencing → resolution → RGB vs multispectral | Merritt |
| 3 | **Raster vs vector, and ready-made datasets** — plus Open Buildings, OSM, GHSL | Merritt |
| 4 | **Choosing a sensor** — Landsat, Sentinel-2, Sentinel-1, VIIRS individually, then the trade-off table: resolution vs revisit vs cost vs cloud-penetration. Keep the cloud-cover failure slide | Prabhmeet |
| 5 | **The tool landscape** — QGIS, ArcGIS, Earth Engine, Python, R. What each is for? | Prabhmeet |
| 6 | **How to see water** — Nsanje framed operationally: *aid is limited, which households do we reach?* Why "just look at it" fails on muddy floodwater. Then histograms and thresholds | Prabhmeet |

Block 6 leads into the practical activity, so it's important we get to it.

**Break the lecture roughly at the halfway mark.** Stand up, stretch.

#### What we can re-use from Satej's lecture last year

Day 1 is meant to go back over the ground we covered in Blantyre. We can't cover all of it, so here's what I propose keeping. 

| 2025 material | 2026 |
|---|---|
| Deck 1A — use cases (poverty map, floods, crop mapping) | **Retained**, compressed to a short opening |
| 2B 3–17 — EM spectrum, reflectance, source→surface→sensor, raster post-processing, georeferencing, resolution, band combination | **Retained** The core of Lecture 1 |
| 2B 6–9 — water vs vegetation reflectance | **Retained**, moved to where it sets up the flood work |
| 2B 34 — ready-made datasets (Open Buildings, OSM, GHSL) | **Retained.** Open Buildings is used in Stage D the same afternoon; OSM in three Day 3 projects |
| 2B 35–36 — raster vs vector | **Retained**, then reinforced hands-on in Stage A |
| 2B 18–33 — seven sensor profiles | **Retained** (Landsat, S2, S1, VIIRS) plus a trade-off table. CHIRPS and MODIS drop to a mention — they reappear in Day 3 project 5. Cloud-cover failure slide kept |
| 2B 42–47 — tool survey (ArcGIS, GEE, geopandas, sf) | **Retained**, brief |
| 2B 59–98 — flood exercise and spatial join | **Retained**, and given the whole afternoon |
| 2B 71–82 — NDWI / SAR / SAR+DEM / flood risk maps | **Retained**, and added as a tail to the flood exercise (Stage C) |
| 2B 37–39 — file formats, providers, aerial/drone | **Moved to Day 3** |
| 2B 48 — resources | **Moved to Day 3** |

### Exercise 1 — four stages
One continuous exercise carried through the day. Each stage ends at a shipped `.qgz` checkpoint so anyone who falls behind rejoins at the next boundary rather than dropping out for the day.

**Stage A — QGIS, taught on the flood data.** This replaces last year's standalone Exercise 0, which depended on OSM and Google Satellite XYZ tiles.
1. Interface tour — panels, layers, toolbars. Slowly.
2. Load `Nsanje_Landsat8_RGB_preflood`; pan, zoom, watch pixels appear at high zoom.
3. Load GADM admin-2 boundaries over it; layer order, transparency, opacity. They see the difference between vector and raster directly.
4. Attribute table; select Nsanje; select Zomba (they're standing in it).
5. Symbology: RGB composite vs single-band grey; min/max stretch on the NIR band.
6. CRS: layer CRS vs project CRS.
7. Save as `.qgz`, close QGIS, reopen, to show anyone who fell behind how to catch up. 

**Stage B — NIR flood detection.** *(First expression field of the workshop.)* Properties → Histogram → Compute → Raster Calculator
`Nsanje_Landsat8_NIR_preflood@1 < 10000` → Symbology, Paletted/Unique values, Classify, delete the 0 class. Then repeat for post-flood and stack to compare.

**Stage C — complicating NIR, introducing SAR**
Pose it as a hypothetical: *rain causes flooding, and rain comes with clouds — so what happens when the day you need imagery is a cloudy one?* 
Put a cloud-covered scene on the projector and ask what they would do. Pairs, then report back, then synthesis. 
Steer toward floods come with storms, storms come with clouds, optical sensors cannot see through cloud, 
and a 16-day revisit means the next clear scene may arrive after the water has receded. 
Then **SAR on the projector**: active sensing, sends its own signal, works at night and through
cloud, smooth water reflects away so water is dark, and it looks strange (speckle, no
intuitive colours) which is normal. Show the same threshold workflow on Sentinel-1 and put the
two water masks side by side. Then ask them to compare what they see: where do they agree, where
do they disagree, which would you trust, and what benefits does each ahve? NIR is easy to interpret
and easy to explain to a non-specialist, but it is weather-dependent. SAR is all-weather and
works at night, but it is noisier and much harder to read. Which one you use depends on
whether you can afford to wait for a clear sky. They watch rather than click through it
themselves. Ship the SAR data and a written walkthrough anyway, so anyone can redo it later or on Day 3.

**Stage D — the deliverable.** *(Second expression field.)* Export the post-flood water raster → **Raster ▸ Conversion ▸ Polygonize** 
 I think the order is this, but I'll produce a document that details all the steps here
→ filter `"DN" == 1` → load `nsanje_buildings.shp` → **Processing Toolbox ▸ Vector general 
▸ Join attributes by location** (buildings first, flood second, "discard records that could not be joined" checked) 
→ read the count off the attribute table → export to CSV.

---

## Day 2 — Tuesday 6 October
### Poverty mapping

| Block | Content |
|---|---|
| **1** | Recap + **Day 1 overflow** · **Lecture 2** start, hopefully finish |
| **2** | **Lecture 2** concludes if necessary· **Exercise 2 · Stage A** begins |
| **3** | **Exercise 2** — Stages A and B |
| **4** | **Code demo** · **Day 3 project menu — choose and scope** |

**Priority order**
- We want everyone to finish the poverty map, and every participant having chosen and scoped a Day 3 project.
- If tight on time, we can cut Stage B's second classification scheme
- We can also cut the code demo, I think that actually might be the first thing I cut since it's not clear to me they will take anything aaway from that

### Lecture 2 — split between instructors

*From imagery to welfare* (Merritt). NSO already understands small-area estimation — census plus survey. This is the same logic with imagery standing in for the census, 
which means estimates can be refreshed between census rounds instead of waiting ten years. Then the mechanics: survey clusters give training labels → extract imagery features at those
locations → fit → predict everywhere. What is actually visible that tracks welfare — roof material, building size and density, road access, nightlights, cropland. Then the 
limits of poverty maps: only as good as the training survey, degrades over time and across regions, cannot see income, and uncertainty at small areas is larger than the map implies.

**Live demo of poverty map** (Prabhmeet). Prabhmeet showing QGIS on the projector, everyone
watches, then they do the same thing themselves in Stage B. No code.

We have household level data with lat/longs, household ids and a consumption measure, covering a
lot of the country from wave 2. It is not a nationally representative sample and it overrepresents urban
households. We'll build a poverty map using that data, which will give us a map that's wrong in a specific, explainable direction.

**Representativity** If you take these households, average consumption
by district or EA or whatever the lowest granularity we can afford, and colour the districts in, the result is biased. Urban households are
overrepresented and urban consumption is higher, so district averages get pulled upward and the
map understates poverty. The bias isn't uniform either: it's worst in the districts where the
urban share of our sample is most inflated relative to the real urban share of that district, so
the map is wrong by different amounts in different places, which is much harder to reason about
than a constant offset. 

The fix is reweighting. If you know the true urban and rural population shares per district, from
the census, you can post-stratify: weight the urban and rural households in each district back to
their real proportions. 

We should be clear about the fact that we can't do it with our data, we need external information about
what the population actually looks like. 

**Coverage.** Some districts will have plenty
of households and some will have very few. Before mapping consumption at all, map the count of
households per district. Never make a choropleth without first looking at how many 
observations are behind each cell. Then pick a threshold below which we suppress, and discuss why that threshold.

**Aggregation.** The same points aggregated to districts give one answer and aggregated to TAs
give another, and TAs will have far more thin or empty units. This is the modifiable areal unit
problem. It's a tradeoff between spatial detail and reliability.

**Points versus areas.** They see the raw households first, coloured by consumption, and only
then aggregate. Aggregation that discards information.

**Direct estimates versus model predictions.** Where we have households we have a direct
estimate, noisy in proportion to how few of them there are. Where we have none we have nothing,
unless we model it using covariates available everywhere, which is what the code demo shows. Both
end up as a colored district on the map and they look identical. Direct estimates are unbiased but the variance blows up
in small samples; model based estimates have lower variance but carry bias that doesn't show.

**Are the differences distinguishable.** With small district samples the confidence intervals get
wide, and adjacent categories on the map frequently overlap. 

**Binning.** Quintiles are ordinal by construction, so they exist whether or not the differences
are real, and they throw away magnitude, so a country with tiny dispersion and one with huge
dispersion produce the same looking map. Bins that mean something outside the data, like above
and below the national poverty rate or a programme eligibility cutoff, usually answer a more
useful question.

### Exercise 2 — two stages

**Stage A: load the households, then look at coverage before anything else.**

Load the household CSV as a point layer, using Delimited Text with the lat/long columns as X and
Y. 

Then look at where the points are. The urban clustering should be visible.

Then load GADM districts and count households per district, and map the count. This is the
coverage map. Discussion: which districts can we say anything about, and where would we refuse to report a number? I 
said we should have this discussion in the lecture, but maybe it fits better here.

**Stage B: make the biased map, then see the corrected one.**

Aggregate consumption to district means. Everyone produces a national poverty map from the data.

Then reveal the post-stratified version, prepared in advance, next to theirs. Same households,
reweighted to the true urban and rural shares per district, and an obviously different map. Ask
which districts moved and why, and let them connect it back to the urban skew they saw on screen
in Stage A.

**Prep note.** Participants shouldn't have to compute weights in QGIS, which is fiddly and not
the lesson. Build the post-stratified layer beforehand and ship it as a styled layer they add at
the reveal. What they do by hand is the naive aggregation.

**Code demo — the only code in the workshop.** Projector only. Walk through the pipeline:
survey points in, satellite covariates extracted, model fitted, predictions written for every
location. The goal is demystification. Pre-run notebook, outputs already saved, nothing executes live.

**Project selection — do this on Day 2.** Introduce the five mini-projects, revisit
their Day 1 goals, let them choose, then scope in pairs on the one-page template. Ideally put the correct data 
on their machines before they go home. 
---

## Day 3 — Wednesday 7 October
### Their own projects

| Block | Content |
|---|---|
| **1** | Recap · **Lecture 3** — Can a satellite answer this? |
| **2** | **Project work** |
| **3** | **Project work** · doubles as the spillover buffer |
| **4** | **Report-backs** · Wrap, resources, certificates |

**Priority order**
- Must finish: report-backs. Everyone presents something, however unfinished.
- This day is the shock absorber for the whole workshop.
- Lecture 3 is the shortest of the three. Day 3's value is in project time and in catching spillover.

### Lecture 3 — the enabling lecture for the afternoon

1. **Can a satellite answer this?** A triage they can apply on their own afterward:
   - **Directly observable** — water extent, buildings, roads, vegetation, bare soil, fire, light
     at night, land cover change.
   - **Inferable with ground truth** — poverty, population, crop yield, building use. Needs survey
     data to train and validate against.
   - **Not observable** — income, prices, attitudes, who is inside a building, and **tourism
     directly**.

2. **Tourism as the worked example, since that's the only specific topic interest I've heard** 
   *Could* proxy: VIIRS nightlights at known lodge and resort locations and their seasonality;
   built-up expansion near Lake Malawi, Liwonde, Mulanje, Cape Maclear; OSM accommodation POIs as
   an infrastructure inventory; road and parking-area detection; vehicle counts in
   very-high-resolution commercial imagery.
   *Cannot* get from satellite, could get from CDR: visitor numbers, nationality, length of stay, spend, occupancy.
   **Honest conclusion:** satellites map tourism infrastructure and its growth well, detect
   seasonality weakly, and cannot count tourists. Point at what would actually answer their
   question — immigration records, hotel returns, mobile roaming data.
   Mini-project 1 lets anyone who wants to test this see it for themselves.

3. **Where data comes from.** Copernicus Browser, USGS EarthExplorer, WorldPop, Geofabrik OSM
   extracts, Open Buildings, ESA WorldCover, CHIRPS. What each costs (nothing), what registration
   each needs, roughly how big the files are.
   Treat this as a handout walkthrough. Walk through the first page on the projector.

### Project work NOTE: THIS MAY BE WAY TOO MUCH WORK, WE MAY WANT TO SCOPE DOWN 

Five pre-scoped mini-projects, each self-contained, each with data already on the drive and its
own short handout. Each reuses Day 1–2 skills and produces an artifact.

| # | Project | Reuses | Artifact |
|---|---|---|---|
| **1** | **Tourism infrastructure** — nightlights over time at lodge/resort locations around Lake Malawi and Liwonde, plus OSM accommodation POIs and built-up change | Raster loading, symbology, zonal statistics, attribute joins, **supplied console snippet** | Tourism infrastructure map + a nightlights trend table |
| **2** | **Urban growth** — built-up expansion in Lilongwe, Blantyre or Zomba between two epochs | Raster differencing, polygonize, spatial join | Growth map + area statistics |
| **3** | **Population and access** — how many people live more than 5 km from a health facility | Zonal statistics, vector buffers, spatial join | Access map + population counts |
| **4** | **Flooding in another district** — repeat the Day 1 workflow on Chikwawa, Salima or Karonga | Everything from Day 1, directly | Flood extent + affected buildings for a new district |
| **5** | **Agricultural seasonality** — NDVI by district through the season, against CHIRPS rainfall | Zonal statistics, time series, charting, **supplied console snippet** | Seasonality chart + map by district |

Project 4 is the safety net: it is the Day 1 workflow on new data, so anyone who struggled on
Day 1 gets a second pass and still finishes with something.


**Report-backs at the end** A few minutes per pair: what they asked, what they found, what they'd need to do it properly.

---

## Success criteria

- **End of Day 1** — every participant has a CSV of flood-affected buildings.
- **End of Day 2** — every participant has an exported poverty map, and has chosen and scoped a
  Day 3 project.
- **End of Day 3** — every participant has a project artifact and has presented it.
- **Take home** — working QGIS, all data, all handouts as PDFs, the data-sources guide, and the
  four mini-projects they *didn't* do, on their own machine.
