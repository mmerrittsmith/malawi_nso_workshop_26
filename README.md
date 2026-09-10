# Satellite Imagery for Measurement — Malawi NSO
**Zomba · 5–7 October 2026**

Three-day, fully offline, hands-on training for the Malawi National Statistical Office on using
satellite imagery for measurement. QGIS is the only tool participants use.

| | |
|---|---|
| **Where / when** | Zomba, Malawi · 5–7 October 2026 |
| **Instructors** | Merritt Smith (UC Berkeley), Prabhmeet Kaur Matta (UC San Diego) |
| **Participants** | 5–10 expected, 15 maximum. Largely non-technical. |
| **Tool** | QGIS — GUI only, potentially some participant coding but only with walkthroughs |
| **Connectivity** | Everything ships on flash drives. |

## Documents

| File | What it is |
|---|---|
| [`agenda.md`](agenda.md) | The workshop outline — full 3-day schedule, session by session |
| [`work_split.md`](work_split.md) | 50:50 preparation assignments, plus known defects in the 2025 materials |
| [`prep/checklist.md`](prep/checklist.md) | Pre-travel checklist: questions for NSO, build tasks, flash drives, verification |
| [`prep/data_audit.md`](prep/data_audit.md) | What's wrong with the inherited exercise data, verified with `gdalinfo` |

## Shape of the workshop

All three days run ~09:00 → 16:00, in four blocks separated by two teas and lunch. Each day is a lecture in the morning and one exercise filling the rest. 

Blocks are drafts, we don't have to fully commit to them being only in those time slots. `agenda.md` gives each day a priority order about what must finish, what flexes, and what to drop first.
A minute-by-minute schedule is probably a fool's errand. We will definitely have to play by ear at points.

| Day | Topic | Participants leave with |
|---|---|---|
| **1 · Mon 5 Oct** | QGIS + flood detection (Nsanje) | A CSV of flood-affected buildings |
| **2 · Tue 6 Oct** | Poverty mapping | An exported poverty map |
| **3 · Wed 7 Oct** | Their own project, from a menu of five | A finished project of their choosing |

Day 3's afternoon doubles as the **spillover buffer** for Days 1–2.

## Two constraints that drive every decision

**Pacing.** Last year we badly overestimated both participant ability and how fast a group gets
through an exercise. The 2025 materials budgeted ~45 minutes for the flood exercise and ~35 for
the spatial join; reality is multiples of that. Hence one exercise per day, and priority orders in place
of schedules. All inherited timing estimates should be ignored.

**Day 1 re-treads last year's ground, at full pace.** Covering the same topics as Blantyre 2025
is deliberate — it is the foundation the rest sits on. That governs what Day 1 covers. The pace is a
separate question: some participants attended last year, some didn't, and nobody should be
assumed to remember any of it. Teach it from scratch.

> **Day 1 is the fullest day** — install, the longest lecture, and the entire flood exercise.
> Its priority order in `agenda.md` matters more than any other: the buildings CSV must get made,
> the Stage C discussion must happen, and the post-flood repetition is the first thing to drop.

## Inherited materials

`malawi workshop 2025/` holds the August 2025 Blantyre workshop ("Harnessing Big Data for
National Statistics", NSO / UC Berkeley / World Bank). That workshop was two days, larger, and
split across satellite and phone data. This one is narrower and deeper.

Reused here:
- `2B - Introduction to Geospatial Data Analysis.pptx` — 99 slides, the core asset. **Use the
  16:9 version** (modified 9 Dec 2025); ignore the `(4_3)` twin.
- `1A - ... Example Use Cases.pptx` — Blantyre poverty map, Nsanje floods, crop mapping
- `1B - Installing QGIS and Anaconda.pptx` — keep the QGIS screens, drop Anaconda
- `Remote Sensing Handout.docx` — the template for all 2026 handouts
- `activity sessions/QGIS Activity/` — Nsanje rasters + 36,077 Open Buildings polygons

Not reused: `2A - Software Systems...` (no room, different purpose), and the CDR and PMT
activity sessions (this workshop is satellite imagery only).

**Read the defects table in `work_split.md` before editing any 2025 deck**

## Other repo assets used

Paths relative to `../` (i.e. `Berkeley/projects/malawi/`):

- `gadm41_MWI_shp/` — GADM 4.1 Malawi admin levels 0–3. Basis of the Day 2 poverty map.
- `mwi_pmt/` — PMT pipeline; source material for the Day 2 code demo.
- `ingest_data/`, `side_projects/recompute_consumption_aggregate/` — IHS-V modules and a working
  consumption-aggregate pipeline. Fallback source for district consumption estimates if NSO's
  own published figures aren't available.
