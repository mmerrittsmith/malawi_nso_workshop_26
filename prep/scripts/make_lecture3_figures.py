#!/usr/bin/env python3
"""Render the figures for Lecture 3 from the workshop's own data.

Writes day3_projects/lecture3/figures/*.png at slide resolution. Every figure is something the
participants will have made or seen the day before, so the lecture argues from their own week.

Run: python3 prep/scripts/make_lecture3_figures.py
"""
import os
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "day3_projects", "lecture3", "figures")
TMP = os.environ.get("TMPDIR", "/tmp") + "/lecture3"
QGIS = "/Applications/QGIS.app/Contents/MacOS/qgis_process"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13})

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  ! failed:", " ".join(cmd[:4]), r.stderr.strip()[:200])
    return r.returncode == 0

def render_project(qgz, extent, out_png, mupp=12):
    """Render a QGIS project to PNG through a GeoTIFF."""
    tif = os.path.join(TMP, os.path.basename(out_png).replace(".png", ".tif"))
    ok = run([QGIS, "run", "native:rasterize", f"--PROJECT_PATH={qgz}", "--",
              f"EXTENT={extent} [EPSG:32736]", f"MAP_UNITS_PER_PIXEL={mupp}", f"OUTPUT={tif}"])
    if ok:
        run(["gdal_translate", "-q", "-of", "PNG", "-outsize", "1200", "0", tif, out_png])
        for junk in (out_png + ".aux.xml", tif + ".aux.xml"):
            if os.path.exists(junk):
                os.remove(junk)
    return ok

def crop(src, box, out_png, size=900, scale=None):
    """Crop a raster to a box (xmin ymin xmax ymax) and write a PNG."""
    cmd = ["gdal_translate", "-q", "-projwin", str(box[0]), str(box[3]), str(box[2]), str(box[1])]
    if scale:
        cmd += ["-ot", "Byte", "-scale", str(scale[0]), str(scale[1]), "1", "255"]
    cmd += ["-outsize", str(size), "0", "-of", "PNG", src, out_png]
    ok = run(cmd)
    if os.path.exists(out_png + ".aux.xml"):
        os.remove(out_png + ".aux.xml")
    return ok

def panels(images, titles, out_name, suptitle=None, figsize=None):
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=figsize or (6.2 * n, 6.6), dpi=150)
    if n == 1:
        axes = [axes]
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(mpimg.imread(img))
        ax.set_title(title, fontsize=15)
        ax.axis("off")
    if suptitle:
        fig.suptitle(suptitle, fontsize=18)
    fig.tight_layout(rect=[0, 0, 1, 0.93] if suptitle else None)
    path = os.path.join(OUT, out_name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", os.path.basename(path))

D1 = os.path.join(ROOT, "day1_floods")
P1 = os.path.join(ROOT, "day3_projects", "project1_tourism")
P2 = os.path.join(ROOT, "day3_projects", "project2_zomba_urban_growth")
P4 = os.path.join(ROOT, "day3_projects", "project4_chikwawa_flood")

# ---------------------------------------------------------------- 1. directly observable: water
print("1. flood water (directly observable)")
render_project(os.path.join(D1, "checkpoints", "day1_stage_D.qgz"),
               "731000,749000,8118000,8136000", os.path.join(TMP, "flood.png"), mupp=20)
crop(os.path.join(D1, "activity", "Nsanje_Landsat8_RGB_postflood.tif"),
     (731000, 8118000, 749000, 8136000), os.path.join(TMP, "flood_plain.png"), scale=(7000, 16000))
panels([os.path.join(TMP, "flood_plain.png"), os.path.join(TMP, "flood.png")],
       ["What the satellite saw", "What we measured: water, and the buildings in it"],
       "01_directly_observable_flood.png",
       "Directly observable — Nsanje, 14 March 2025")

# ---------------------------------------------------------------- 2. the threshold decides
print("2. threshold sensitivity (Chikwawa)")
nir = os.path.join(P4, "Chikwawa_Landsat8_NIR_postflood.tif")
raw = os.path.join(TMP, "chik_nir.bin")
run(["gdal_translate", "-q", "-of", "ENVI", nir, raw])
a = np.fromfile(raw, dtype=np.uint16).reshape(1008, 1008)
# the colour image as the base, so the flood reads as a place rather than a grey field
crop(os.path.join(P4, "Chikwawa_Landsat8_RGB_postflood.tif"),
     (691665, 8175475, 721905, 8205715), os.path.join(TMP, "chik_rgb.png"),
     size=1008, scale=(7000, 16000))
base = mpimg.imread(os.path.join(TMP, "chik_rgb.png"))
fig, axes = plt.subplots(1, 3, figsize=(18, 7.2), dpi=150)
for ax, thr, count in zip(axes, (9000, 10000, 11000), (12, 55, 156)):
    ax.imshow(base)
    water = np.ma.masked_where(a >= thr, np.ones_like(a, dtype=float))
    ax.imshow(water, cmap="cool", alpha=0.9, vmin=0, vmax=1)
    ax.set_title(f"water = below {thr:,}\n{count} flooded buildings", fontsize=16)
    ax.axis("off")
fig.suptitle("The same image, three defensible cut-offs — Chikwawa", fontsize=19)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(OUT, "02_threshold_decides_the_answer.png"), bbox_inches="tight")
plt.close(fig)
print("  wrote 02_threshold_decides_the_answer.png")

# ---------------------------------------------------------------- 3. dry soil looks like roofs
print("3. the dry-soil trap (Zomba)")
# the whole Zomba square the participants work in on Day 3, so the percentages here are the same
# ones that appear in the project 2 handout
box = (739020, 8287750, 759020, 8307750)


def to_array(src, dtype=np.int16):
    """Crop to the box and read as numpy, via ENVI (the python GDAL bindings are broken here)."""
    dst = os.path.join(TMP, "z_" + os.path.basename(src).replace(".tif", ".bin"))
    run(["gdal_translate", "-q", "-projwin", str(box[0]), str(box[3]), str(box[2]), str(box[1]),
         "-of", "ENVI", src, dst])
    a = np.fromfile(dst, dtype=dtype).astype(float)
    return a.reshape(int(np.sqrt(a.size)), -1)


nirz = to_array(os.path.join(P2, "Zomba_Sentinel2_NIR_20160730.tif"))
swirz = to_array(os.path.join(P2, "Zomba_Sentinel2_SWIR_20160730.tif"))
ndbi = (swirz - nirz) / np.maximum(swirz + nirz, 1)
ghsl = to_array(os.path.join(P2, "Zomba_builtup_2015_GHSL.tif"), dtype=np.uint16)
pct_index = 100 * (ndbi > 0).mean()
pct_layer = 100 * ghsl.sum() / (ghsl.size * 100 * 100)   # m2 built per 100 m cell
print(f"  index says {pct_index:.0f}%, layer says {pct_layer:.1f}%")

# one base picture under all three panels, so the eye compares claims and not pictures
crop(os.path.join(P2, "Zomba_Sentinel2_RGB_20160730.tif"), box, os.path.join(TMP, "z_rgb.png"),
     size=1000, scale=(1, 3000))
zbase = mpimg.imread(os.path.join(TMP, "z_rgb.png"))
span = [0, zbase.shape[1], zbase.shape[0], 0]
fig, axes = plt.subplots(1, 3, figsize=(18.6, 7.0), dpi=150)
for ax in axes:
    ax.imshow(zbase, extent=span)
    ax.axis("off")
axes[0].set_title("Zomba, July 2016", fontsize=16)
axes[1].imshow(np.ma.masked_where(ndbi <= 0, np.ones_like(ndbi)), cmap="autumn",
               alpha=0.75, vmin=0, vmax=1, extent=span, interpolation="nearest")
axes[1].set_title(f"A built-up index calls this built-up\n{pct_index:.0f}% of the square",
                  fontsize=16)
# magma, as on the project 2 checkpoints, but with the alpha carrying the value too: a cell that is
# 2% roof should barely show, or the panel argues against its own caption
shade = plt.cm.magma(np.clip(ghsl / 5000, 0, 1))
shade[..., 3] = np.clip(ghsl / 2000, 0, 1)
axes[2].imshow(shade, extent=span, interpolation="nearest")
axes[2].set_title(f"The built-up layer says\n{pct_layer:.0f}%", fontsize=16)
fig.suptitle("Dry soil reflects like a roof — the obvious method fails", fontsize=19)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(os.path.join(OUT, "03_dry_soil_trap.png"), bbox_inches="tight")
plt.close(fig)
print("  wrote 03_dry_soil_trap.png")

# ---------------------------------------------------------------- 4. a signal that misleads
print("4. Likoma lights (a signal appearing is not the thing appearing)")
# zonal sum of night lights in each stop's 3 km circle, one value per year: exactly what the
# supplied snippet gives the participants in Extension B. Checked against qgis_process.
years = list(range(2012, 2023))
likoma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 24.6, 22.9]
senga = [30.1, 24.2, 19.7, 24.6, 22.7, 32.3, 38.1, 39.2, 42.3, 47.1, 40.0]
fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
ax.plot(years, likoma, "o-", lw=3, ms=9, color="#b73779", label="Likoma Island")
ax.plot(years, senga, "o-", lw=3, ms=9, color="#777777", label="Senga Bay")
ax.axvspan(2019.6, 2021.4, color="#cccccc", alpha=0.5)
ax.set_ylim(-2, 60)
ax.text(2020.5, 54, "COVID:\nalmost no visitors", ha="center", fontsize=13)
ax.set_xlabel("year"), ax.set_ylabel("night lights in the 3 km circle")
ax.set_title("Likoma's lights switch on in 2021", fontsize=17)
ax.legend(frameon=False)
for side_name in ("top", "right"):
    ax.spines[side_name].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "04_likoma_lights_mislead.png"), bbox_inches="tight")
plt.close(fig)
print("  wrote 04_likoma_lights_mislead.png")

# ---------------------------------------------------------------- 5. no signal is not no activity
print("5. Nkhotakota (no signal, real lodge)")
for tag, centre in (("tongole", (34.0503, -12.9112)), ("capemac", (34.8493, -14.0166))):
    p = subprocess.run(["gdaltransform", "-s_srs", "EPSG:4326", "-t_srs", "EPSG:32736"],
                       input=f"{centre[0]} {centre[1]}\n", capture_output=True, text=True).stdout.split()
    cx, cy = float(p[0]), float(p[1])
    crop(os.path.join(P1, "Sentinel2_2025.tif"),
         (cx - 2500, cy - 2500, cx + 2500, cy + 2500), os.path.join(TMP, f"{tag}.png"))
panels([os.path.join(TMP, "tongole.png"), os.path.join(TMP, "capemac.png")],
       ["Nkhotakota: 1 lodge, 20 people,\nno lights, 3 mapped buildings",
        "Cape Maclear: 25 lodges, 2,866 buildings,\nlit in both years"],
       "05_no_signal_is_not_no_activity.png",
       "Both are tourism. Only one leaves a mark a satellite can see.")

print("\nfigures in", OUT)
