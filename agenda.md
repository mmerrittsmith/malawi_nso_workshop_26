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

All three days run from around **09:00 → 16:00**.

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

**1. One exercise per day.** Last year we badly overestimated group pace. 

**2. Day 1 will re-hash last year's material, but teach it as if it was new.** Don't lie to them and tell them it's new, I just mean we shouldn't assume they remember anything.
We want to establish a common foundation and make sure everyone is starting from the same place on the exercises, since we don't know the composition of the room in advance this time. 

**3. Assume no internet.** 

**4. No participant coding.** In general, I think we can allow for some coding in QGIS in guided exercises, but we don't have time to teach them to code.

*What that means in practice:*
- **Expression fields are fair game throughout.** Day 1 already teaches two of them — the Raster
  Calculator (`Nsanje_Landsat8_NIR_preflood@1 < 10000`) in Stage B and the vector Filter
  (`"DN" == 1`) in Stage D, both inherited unchanged from the 2025 handout. By Day 3 an
  expression box is familiar ground, so Field Calculator and Select-by-expression can be used
  freely in the projects.
- **The Python console appears in only one place:** a supplied, ready-to-run snippet that
  loops zonal statistics over a time series.They don't write it, they're just shown it.
- **Nobody is taught to program.** The snippet is a labeled tool, and the handout says so.

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
- If VERY short on time, we can shrink SAR to the slides only and skip the extension
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
| 4 | **Choosing a sensor** — Landsat, Sentinel-2, Sentinel-1, VIIRS individually, then the trade-off table: resolution vs revisit vs cost vs cloud-penetration. Keep the cloud-cover failure slide | Merritt |
| 5 | **The tool landscape** — QGIS, ArcGIS, Earth Engine, Python, R. What each is for? | Merritt |
| 6 | **How to see water** — Nsanje framed operationally: *aid is limited, which households do we reach?* Why "just look at it" fails on muddy floodwater. Then histograms and thresholds | Merritt |

Block 6 leads into the practical activity, so it's important we get to it.

**Break the lecture roughly at the halfway mark.** Stand up, stretch.

#### Block 1 — why we care

**Three questions an NSO gets asked.** One slide, and it sets up the whole week:
1. **After a flood, how many households were affected, and where?** → Day 1
2. **Where is poverty concentrated, below the district level?** → Day 2
3. **How is land use changing** — cities spreading, cropland shifting? → Day 3 (projects 2 and 5)

We answer the first two together this week. The third is on the Day 3 menu for anyone who wants it.

**Why the usual tools struggle with these.** Frame it in terms they already work with:
- **Census:** complete coverage, but once a decade. Malawi's last was 2018, so by October 2026 it's
  eight years old.
- **Household surveys (IHS):** current, but the sample is designed for national and district
  estimates. Below that there are too few households to report a number.
- **Field assessments after a disaster:** accurate, but slow and expensive, and the flooded areas
  are the hardest ones to reach.
- **Satellite imagery:** covers everywhere, repeats every few days to weeks, and the sensors we
  use are free. But it measures *surfaces*, not people. That's why every example this week pairs
  imagery with something on the ground: building footprints on Day 1, survey data on Day 2.

Close the framing with: *an estimate from imagery is still an estimate, with error, like a
survey.* Day 2 is about that error.

**Anchors, from Lecture Part A:**
- **Floods:** Nsanje dry season vs wet season (slides 14–18). Stop there; slides 19–20 (muddy
  water vs soil, then the extra signal that separates them) belong in block 6.
- **Poverty:** Blantyre, ~1,300 survey points → consumption estimates for 178,810 households
  (4–9). Slide 9 (targeting and measurement) is the payoff for an NSO audience.
- **Land use:** field boundaries and crop types (10–13). The crop legend (barley, canola, alfalfa)
  isn't from Malawi, so say it's an example from elsewhere.
- **Preview of today:** slide 21. Update its bullets to match Exercise 1's four stages, and note
  the export is a CSV (it opens in Excel).

#### Block 4 — choosing a sensor

Sensor profiles are Part B 22–37: Landsat, Sentinel-2 (including the cloud-cover slide, 27),
Sentinel-1, VIIRS, then CHIRPS and MODIS. CHIRPS and MODIS stay in and get covered quickly; both come
back in project 5. The trade-off table is slide 42:

| Sensor | Pixel | Revisit | Through clouds? | Cost |
|---|---|---|---|---|
| **Landsat 8 & 9** | 30 m | 16 days each, 8 days combined | No | Free |
| **Sentinel-2** | 10 m for red, green, blue and near-infrared; 20–60 m for the rest | 5 days at the equator | No | Free |
| **Sentinel-1** (radar) | 10 m | 6 days | Yes | Free |
| **VIIRS** (night lights) | 750 m | Daily | No | Free |

For reference, not slide material: Sentinel-1's 10 m is pixel spacing, with ~20 m true resolution;
VIIRS composites sit on a ~500 m grid; MODIS is 250 m–1 km every 1–2 days; CHIRPS is a 0.05° grid
(~5.5 km), satellite infrared plus rain gauges, 1981 to present.

**Changes worth knowing about in 2026** (not slide material, but they affect the data guide and
Day 3):
- **Sentinel-1** is back to two satellites. Sentinel-1B failed in December 2021, leaving 1A alone
  on a 12-day cycle. Sentinel-1C has been fully operational since May 2025, and 1D since April 2026;
  the 6-day cycle was re-established on 24 June 2026, and 1A was retired at the end of June.
- **VIIRS:** NOAA stops delivering Suomi NPP data on 1 November 2026. VIIRS continues on NOAA-20
  and NOAA-21, and archived data isn't affected.
- **MODIS:** the Terra and Aqua satellites begin shutting down in late 2026 or early 2027. The
  archive stays available, so project 5's past seasons are fine, but the data-sources guide should
  point to VIIRS for anything going forward.

Sources:
[USGS Landsat 8–9 Collection 2](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-9-operational-land-imager-and) ·
[NASA Landsat 9](https://science.nasa.gov/missions/landsat/landsat-9-to-provide-a-wealth-of-data-to-landsat-archive/) ·
[ESA Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2) ·
[SentiWiki S2 mission](https://sentiwiki.copernicus.eu/web/s2-mission) ·
[SentiWiki S1 mission](https://sentiwiki.copernicus.eu/web/s1-mission) ·
[ESA: Sentinel-1B mission ends](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/Mission_ends_for_Copernicus_Sentinel-1B_satellite) ·
[Sentinel-1 data products](https://sentinel.esa.int/web/sentinel/missions/sentinel-1/data-products) ·
[S1C/D final orbital configuration, 24 Jun 2026](https://dataspace.copernicus.eu/news/2026-6-24-s1cd-final-orbital-configuration-achieved) ·
[EOG VIIRS nighttime lights](https://eogdata.mines.edu/products/vnl/) ·
[VIIRS DNB composites metadata](https://data.opendatascience.eu/geonetwork/static/api/records/e8f02f4a-0f98-44c3-8311-6e45555ef3fb) ·
[NOAA: Suomi NPP data cessation](https://www.nesdis.noaa.gov/news/cessation-of-suomi-national-polar-orbiting-partnership-s-npp-data-users-onafter-november-01-2026) ·
[NASA Earthdata MODIS](https://www.earthdata.nasa.gov/data/instruments/modis) ·
[NASA: MODIS to VIIRS transition](https://www.earthdata.nasa.gov/data/alerts-outages/transition-from-modis-viirs) ·
[CHC CHIRPS](https://www.chc.ucsb.edu/data/chirps) ·
[UCAR Climate Data Guide: CHIRPS v3](https://climatedataguide.ucar.edu/climate-data/chirps-climate-hazards-infrared-precipitation-station-data-version-3)

#### Block 6 — how to see water

Goal: participants read a histogram and call the threshold *before* QGIS opens. Goes right before
the Exercise 1 title slide (Part B 52). About seven slides. The histogram images are in
`day1_floods/lectures/figures/`, made from the actual exercise rasters.

1. **The question for this afternoon.** After the Nsanje flood, aid is limited: which households do
   we reach first? That takes two things: where the buildings are, and where the water is. The
   buildings we have (Open Buildings, slide 38). The water is the hard part.
2. **Can't we just look at it?** Put up an ordinary color (RGB) image of the flooded area. Part A
   slide 19 ("Not obvious how to distinguish between soil and muddy floodwaters") is this slide
   already. Ask the room to point to the water. Muddy floodwater and wet soil
   are both brown, so people disagree, and a map can't be built on people disagreeing.
3. **Water in near-infrared.** Plants reflect near-infrared strongly; water absorbs it. So in the
   near-infrared band, water is dark and almost everything else is bright. Reuse Part B 8–9 here (or
   57, which repeats them), then Part A 20, where the water stands out.
4. **Every pixel is a number.** Tie back to slide 10: each pixel in the near-infrared band has a
   value. In this scene they run from about 7,000 to 26,000 before the flood. Dark (low) means
   likely water.
5. **Reading a histogram:** `nir_hist_preflood_blank.png`. Across the bottom is the value, up the
   side is how many pixels have it. Ask: what's the big hump? (land) What's the small bump on the
   far left? (water) Where would you draw the line between them? Most people point at the dip
   around 10,000.
6. **The threshold:** `nir_hist_preflood.png`. 10,000 sits in the dip. About 1% of the scene falls
   below it.
7. **Call it again after the flood:** `nir_hist_postflood_blank.png`, then `nir_hist_postflood.png`.
   Ask the same question. This time there's no clean dip; the low values are a long flat shoulder
   running into the land hump, because muddy and shallow water blends into wet ground. At the same
   10,000 line, about 3% of the scene is water, three times as much as before. Two points to
   land:
   - **A threshold is a judgment call**, like a poverty line. Move it and the count changes. That
     matters on Day 2 too.
   - **The whole land hump moved right** (brighter) between September and March, most likely
     greener vegetation in the rainy season. Which is why the threshold is checked on each image,
     not copied blindly.

Then slide 52: "This afternoon you'll do exactly this in QGIS."

#### What we can re-use from last year's decks

Two decks in `day1_floods/lectures/`. **Part A** (`Day 1 Lecture Part A.pptx`, 26 slides) is last
year's use-cases deck: Blantyre poverty map, crop mapping, Nsanje floods. **Part B**
(`Day 1 Lecture Part B.pptx`) is last year's 2B deck. Part B numbers are from Merritt's edited
version (92 slides, 13 Sep), listed in deck order.

| Slides | Content | 2026 |
|---|---|---|
| **A** 1–3 | Title, introductions, overview of uses | **Block 1.** Add Prabhmeet's introduction. Title slide says 5–8 October; the workshop is 5–7 |
| **A** 4–9 | Blantyre poverty map | **Block 1** |
| **A** 10–13 | Field boundaries and crop types | **Block 1**, brief |
| **A** 14–18 | Nsanje floods | **Block 1** |
| **A** 19–20 | Muddy water vs soil; extra signal separates them | **Block 6** |
| **A** 21 | Preview of today's technical session | **Retained**, bullets updated to the four stages |
| **A** 22–25 | Flood prediction; urban planning and energy examples | **Cut** |
| **A** 26 | Key points | Optional close for block 1 |
| **B** 1–2 | Title; agenda | Update: title still says 18–19 August 2025, Blantyre; agenda still lists QGIS set-up and the 2025 exercises |
| **B** 3–7, 10–17 | Remote sensing principles, post-processing, resolution, band combination | **Block 2** |
| **B** 8–9 | Water vs vegetation reflectance | **Block 2**, reused in block 6 |
| **B** 18–21 | Why use this data? (three questions, why the usual tools struggle) | **Block 1** content |
| **B** 22–37 | Sensor profiles: Landsat, Sentinel-2 incl. cloud cover, Sentinel-1, VIIRS, CHIRPS, MODIS | **Block 4**; CHIRPS and MODIS covered quickly |
| **B** 38–41 | Ready-made datasets; raster vs vector; layering | **Block 3** |
| **B** 42 | Sensor trade-off table | **Block 4** |
| **B** 43–49 | Tool survey (QGIS, ArcGIS, Earth Engine, geopandas, sf) | **Block 5** |
| **B** 50 | Further resources | **Retained** |
| **B** 51 | Data for exercises (download link) | Link is dead and fails offline; point to the flash drive |
| — | *(new)* How to see water | **Block 6**, see above |
| **B** 52–63 | Flood detection with NIR | **Stages A–B.** The slides are the participant handout, so Stage A needs new slides |
| **B** 64–66 | Cloud-covered imagery | **Stage C** discussion prompt |
| **B** 67–78 | NDWI, SAR, SAR + DEM, flood risk maps, questions, key points | **Stage C** |
| **B** 79–90 | Spatial join with buildings | **Stage D** |
| **B** 91–92 | Key points; Zikomo | Day 1 wrap |

### Exercise 1 — four stages
One continuous exercise carried through the day. Each stage ends at a shipped `.qgz` checkpoint so anyone who falls behind rejoins at the next boundary rather than dropping out for the day.

**Stages A and B are a demonstration.** Merritt drives on the projector, participants watch. They take over at the Stage B checkpoint: everyone opens `day1_stage_B.qgz` from the `checkpoints` folder and works hands-on from Stage C. This replaces last year's standalone Exercise 0, which depended on OSM and Google Satellite XYZ tiles, and it gets the room to the same starting line regardless of how fast anyone types.

Two consequences to plan around:
- **Their first hands-on action is opening a checkpoint.** Walk that one step slowly — Project ▸ Open — because every later fallback depends on it.
- **Their first time loading a file is Stage D** (the buildings). Day 3 projects all begin with loading layers, so don't rush that step; it is the only loading practice they get before then.

**Stage A — QGIS, shown on the flood data.** Demonstrated, not followed along.
1. Interface tour — panels, layers, toolbars. Slowly.
2. Load `Nsanje_Landsat8_RGB_preflood`; pan, zoom, watch pixels appear at high zoom.
3. Load the GADM district boundaries (`gadm41_MWI_1`, admin-1) over it; layer order, transparency, opacity. They see the difference between vector and raster directly. (Not admin-2: in GADM's Malawi data that's traditional authorities, so Nsanje would come up as 11 pieces.)
4. Attribute table; select Nsanje; select Zomba (they're standing in it).
5. Symbology: RGB composite vs single-band gray; min/max stretch on the NIR band.
6. CRS: layer CRS vs project CRS. The imagery is in UTM zone 36S (EPSG:32736), in meters; the districts are in latitude/longitude (EPSG:4326), in degrees. They still line up because QGIS reprojects on the fly. The districts are left in 4326 on purpose so this step has something to show.
7. Save as `.qgz`, close QGIS, reopen, to show anyone who fell behind how to catch up. 

**Stage B — NIR flood detection.** Still demonstrated. *(First expression field of the workshop.)* Properties → Histogram → Compute → Raster Calculator
`Nsanje_Landsat8_NIR_preflood@1 < 10000` → Symbology, Paletted/Unique values, Classify, delete the 0 class. Then repeat for post-flood and stack to compare.

**Stage C — complicating NIR, introducing SAR** *(hands-on from here: everyone opens `day1_stage_B.qgz` first)*
Pose it as a hypothetical: *rain causes flooding, and rain comes with clouds — so what happens when the day you need imagery is a cloudy one?* 
Put a cloud-covered scene on the projector and ask what they would do. Pairs, then report back, then synthesis. 
Steer toward floods come with storms, storms come with clouds, optical sensors cannot see through cloud, 
and an 8–16 day revisit means the next clear scene may arrive after the water has receded. 
Then **SAR on the projector**: active sensing, sends its own signal, works at night and through
cloud, smooth water reflects away so water is dark, and it looks strange (speckle, no
intuitive colors) which is normal. Show the same threshold workflow on Sentinel-1 and put the
two water masks side by side. Then ask them to compare what they see: where do they agree, where
do they disagree, which would you trust, and what benefits does each ahve? NIR is easy to interpret
and easy to explain to a non-specialist, but it is weather-dependent. SAR is all-weather and
works at night, but it is noisier and much harder to read. Which one you use depends on
whether you can afford to wait for a clear sky.

**SAR extension.** Hands-on for anyone ahead of the room, shown on the projector otherwise. The
same Raster Calculator step as Stage B, on `Nsanje_Sentinel1_VV_dB_postflood.tif` (18 Mar 2025,
four days after the Landsat post-flood image): `Nsanje_Sentinel1_VV_dB_postflood@1 < -16`. Values
are radar backscatter in decibels, and water is dark (very negative). Checked on the data:
- **After the flood, −16 dB works.** The histogram has a separate water bump around −20 to −16 dB
  with a dip at −16. About 1.9% of the scene falls below it, and 81% of those pixels are also
  water in the NIR mask.
- **Radar finds only about half the NIR water**, which is the discussion: four days of receding
  water, and flooded vegetation can bounce the radar signal back bright.
- **Don't demo on the pre-flood scene** (`…_preflood.tif`, 7 Sep 2024). There's no water bump, and
  dry bare ground in the dry season is dark to radar too, so the same threshold picks up land.

**Stage D — the deliverable.** *(Second expression field.)* Export the post-flood water raster → **Raster ▸ Conversion ▸ Polygonize** 
→ filter `"DN" == 1` → load `nsanje_buildings.shp` → **Processing Toolbox ▸ Vector general 
▸ Join attributes by location** (buildings first, flood second, "discard records that could not be joined" checked) 
→ read the count off the attribute table → export to CSV. This order matches the 2025 step slides (Lecture Part B 88–96), which become the Stage D handout.
**Expected answer: 108 buildings.** Checked 15 Sep by running these exact steps in QGIS 3.44.14 on the post-flood NIR (1,585 flood polygons, 36,077 buildings). Both join types give 108, so the one-to-many default doesn't double-count here.

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

### Lecture 2 — Prabhmeet

*From imagery to welfare* (Prabhmeet). NSO already understands small-area estimation — census plus survey. This is the same logic with imagery standing in for the census, 
which means estimates can be refreshed between census rounds instead of waiting ten years. Then the mechanics: survey clusters give training labels → extract imagery features at those
locations → fit → predict everywhere. What is actually visible that tracks welfare — roof material, building size and density, road access, nightlights, cropland. Then the 
limits of poverty maps: only as good as the training survey, degrades over time and across regions, cannot see income, and uncertainty at small areas is larger than the map implies.

**Live demo of poverty map** (Prabhmeet). Prabhmeet showing QGIS on the projector, everyone
watches, then they do the same thing themselves in Stage B. No code.

We have household level data with lat/longs, household ids and a consumption measure, covering a
lot of the country from wave 2. It is not a nationally representative sample and it overrepresents urban
households. We'll build a poverty map using that data, which will give us a map that's wrong in a specific, explainable direction.

**Representativity** If you take these households, average consumption
by district or EA or whatever the lowest granularity we can afford, and color the districts in, the result is biased. Urban households are
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

**Points versus areas.** They see the raw households first, colored by consumption, and only
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
and below the national poverty rate or a program eligibility cutoff, usually answer a more
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
| **2** | **Urban growth** — built-up expansion in Zomba, Sentinel-2 on 30 Jul 2016 vs 20 Jul 2026 (20 × 20 km around the city) | Raster differencing, polygonize, spatial join | Growth map + area statistics |
| **3** | **Population and access** — how many people live more than 5 km from a health facility | Zonal statistics, vector buffers, spatial join | Access map + population counts |
| **4** | **Flooding in Chikwawa** — repeat the Day 1 workflow on the same March 2025 flood, 30 × 30 km of the Shire floodplain upstream of Nsanje. Landsat 8, 19 Sep 2024 vs 14 Mar 2025. Expected answer: 55 buildings | Everything from Day 1, directly | Flood extent + affected buildings for a new district |
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
