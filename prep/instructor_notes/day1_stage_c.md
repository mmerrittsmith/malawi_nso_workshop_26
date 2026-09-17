# Day 1, Stage C — discussion plan and SAR script (instructor notes)

**Where it sits:** Block 4, after Stage B (they have their own before/after water layers) and before
Stage D (the spatial join). Budget **25–35 minutes**: about 12 on the discussion, about 15 on the
radar demo. If the room is behind, see "If you're short of time" at the end.

**What it is for.** Stage B taught a method that works. Stage C asks when it *fails*, and shows the
answer a statistical office would actually reach for. Nobody clicks during this stage: they watch,
argue, and come back to their own screens for Stage D.

**On screen:** `day1_stage_C.qgz` from `day1_floods/checkpoints/`. It opens with the post-flood
color image, the Sentinel-1 radar image, and both water layers, so nothing needs loading while
people are waiting.

---

## Part 1 — The hypothetical (about 12 minutes)

**Set it up (2 min).** Say the situation plainly:

> "You did this for a flood in March. Now imagine the district commissioner calls during the next
> flood and needs the number of affected households **this week**. You open the satellite image for
> the day the water peaked, and this is what you get."

Put up **Lecture Part B slides 67–69** (the cloud-covered scene). Let them look at it for a moment
before you say anything else. Then ask the question and stop talking:

> **"What would you do?"**

**Pairs (3 min).** Ask each pair for two answers they could actually carry out. Two forces them past
the first idea, which is usually "wait".

**Report back (4 min).** Take one answer per pair, write each on the board in a couple of words.
Don't evaluate them yet; just collect. Expect some of:

| What they usually say | What to do with it |
|---|---|
| Wait for the next clear image | Good. Ask **how long** they'd wait. Land the revisit numbers below. |
| Use an older image | Ask what question that answers: it shows where water *was*, not where it is now. |
| Use the cloud-free parts only | Good instinct. Ask what happens if the cloud sits over the worst-hit area. |
| Go and look on the ground | Right answer in real life. Ask how long it takes to reach a flooded area, and what that costs. |
| Use a different satellite | This is the door into the radar demo. Ask: what would have to be different about it? |

**Synthesis (3 min).** Draw the chain out loud, and write it on the board:

> floods come with storms → storms come with cloud → optical sensors see cloud, not ground →
> the next clear image may arrive after the water has gone.

The revisit numbers, so "wait for the next image" gets a real cost:

- **Landsat 8 and 9 together:** a new image every **8 days** (16 for either one alone).
- **Sentinel-2:** every **5 days**.
- But that is the *pass*, not a usable image. In the rainy season several passes in a row can be
  clouded out, so the wait can be **weeks**.

Ask the closing question and let it hang: **"So what kind of sensor would not care about cloud?"**

---

## Part 2 — The radar answer (about 15 minutes)

**Explain it before you show it (3 min).** Four sentences, no more:

1. The sensors so far are **passive**: they measure sunlight that bounced off the ground, so cloud
   blocks them and night defeats them.
2. Radar is **active**: the satellite sends its own pulse and listens for the echo, so it works at
   night and the pulse passes through cloud.
3. **Smooth water reflects the pulse away** from the satellite, so open water comes back almost
   silent, which means dark in the image.
4. It looks strange: grainy, no natural colors. That grain (speckle) is normal, not a fault.

**Show the radar image.** Switch to `Sentinel-1 VV dB (post-flood)`, 18 March 2025, four days after
the Landsat image. Let them react to how odd it looks, then point out the dark branching shapes
along the Shire. Ask: **"Where is the water?"** They can usually read it within a few seconds, which
is the point: the shape is recognizable even though the image looks alien.

**Run the same method they just ran.** In **Raster ▸ Raster Calculator**, on the projector:

```
"Nsanje_Sentinel1_VV_dB_postflood@1" < -16
```

Say why the number is different: these are decibels, a measure of how much signal came back, not
brightness. Water is very negative. Everything else about the method is identical to Stage B:
look at the values, pick a cut-off, keep what falls below it.

*(The checkpoint already contains this layer as `SAR water (post-flood)` if the calculator
misbehaves on the day.)*

**Put the two water maps side by side.** Turn on `water_postflood` (from the near-infrared) and the
radar one together. Then run the comparison as a discussion, not a lecture:

> **"Where do they agree? Where do they disagree? Which would you trust?"**

What the data actually shows, so you can steer without guessing:

- **81%** of what radar calls water is also water in the near-infrared map. Where both agree, the
  answer is solid.
- Radar finds only about **half** of the near-infrared water. Two honest reasons: the images are
  **four days apart** and water was receding; and **flooded vegetation** bounces the pulse back
  brightly, so water under crops or trees can read as land.
- On the **pre-flood** scene the same cut-off fails: dry season riverbed and bare sand are also dark
  to radar. **Don't demo that one** — but it is worth saying out loud, because it is the honest
  limit of the method.

**Land the trade-off (3 min).** Write the two columns on the board and let them fill it in:

| | Near-infrared | Radar |
|---|---|---|
| Cloud | Blocked | Sees through |
| Night | No | Yes |
| Easy to read | Yes | No: speckle, no natural colors |
| Easy to explain to a non-specialist | Yes | Harder |
| Confused by | Cloud, shadow | Dry bare ground, flooded vegetation |

**The sentence to end on:** *which one you use depends on whether you can afford to wait for a clear
sky.*

---

## Questions that come up

- **"Can radar see through buildings or trees?"** No. It penetrates cloud, not solid things. Under a
  dense canopy it mostly sees the canopy.
- **"Why is water dark if radar sends its own signal?"** Because a flat surface reflects the pulse
  away from the satellite, like a torch shone at a mirror at an angle. Rough surfaces scatter some
  of it back.
- **"Is the grain an error?"** No. Speckle is how radar images look. Averaging neighboring pixels
  smooths it, at the cost of detail.
- **"Why not always use radar?"** Harder to read, easier to get wrong (see the dry-ground problem),
  and nobody can eyeball it for a sanity check the way they can with a color image.
- **"Is it free?"** Yes: Sentinel-1, from the European Union's Copernicus program.

## If you're short of time

- **Tight:** keep the hypothetical and the pair discussion, skip the live Raster Calculator, and
  show the two finished water layers from the checkpoint. About 15 minutes.
- **Very tight:** slides 67–69 plus slides 70–78, talk through them, and say the data is on the
  drive with a walkthrough for Day 3. About 5 minutes.
- **Never cut:** the chain of reasoning (flood → cloud → optical fails → radar) and the "where do
  they disagree" question. That pair is the whole point of the stage.

## Files

- `day1_floods/checkpoints/day1_stage_C.qgz` — everything below, already loaded and styled
- `day1_floods/activity/Nsanje_Sentinel1_VV_dB_postflood.tif` — radar, 18 Mar 2025 (VV, decibels)
- `day1_floods/activity/Nsanje_Sentinel1_VV_dB_preflood.tif` — radar, 7 Sep 2024 (the one that
  doesn't separate cleanly)
- `day1_floods/checkpoints/data/sar_water_postflood.tif` — the `< -16` result, pre-made
