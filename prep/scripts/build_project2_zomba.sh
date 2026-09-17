#!/bin/bash
# Mini-project 2 data: urban growth in Zomba, Sentinel-2 L2A (Planetary Computer), two dry-season
# dates ten years apart, 0% cloud on both tiles: 2016-07-30 and 2026-07-20.
# Area: 20 x 20 km centered on Zomba City (35.32 E, 15.385 S), EPSG:32736, on Sentinel-2's own
# 10 m grid (no reprojection). Files per date: RGB (B4, B3, B2), NIR (B8), SWIR (B11, 20 m → 10 m
# nearest). Values are surface reflectance x 10000, Int16.
# Harmonized: scenes from processing baseline 04.00 onwards (Jan 2022+) carry a +1000 offset;
# it's removed so 2016 and 2026 values are directly comparable (for NDVI/NDBI thresholds).
set -euo pipefail
export GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR GDAL_HTTP_MAX_RETRY=5 GDAL_HTTP_RETRY_DELAY=5

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/day3_projects/project2_zomba_urban_growth"
RAW="$ROOT/data_library/_raw/project2"
mkdir -p "$OUT" "$RAW"
STAC=https://planetarycomputer.microsoft.com/api/stac/v1
CO="-co COMPRESS=DEFLATE -co PREDICTOR=2 -co TILED=YES"

# 20 km square snapped to the 10 m grid
read CX CY < <(echo "35.32 -15.385" | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:32736 | awk '{print $1, $2}')
X0=$(python3 -c "print(int(round(($CX-10000)/10))*10)"); Y1=$(python3 -c "print(int(round(($CY+10000)/10))*10)")
TE="$X0 $((Y1-20000)) $((X0+20000)) $Y1"
echo "extent: $TE"

TOK=$(curl -sS -m 60 https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

for d in 2016-07-30 2026-07-20; do
  tag=${d//-/}
  curl -sS -m 90 -X POST "$STAC/search" -H 'Content-Type: application/json' \
    -d "{\"collections\":[\"sentinel-2-l2a\"],\"bbox\":[35.2,-15.48,35.44,-15.29],\"datetime\":\"${d}T00:00:00Z/${d}T23:59:59Z\",\"limit\":20}" \
    > "$RAW/items_$tag.json"
  TOK="$TOK" python3 - "$RAW/items_$tag.json" "$RAW" "$tag" <<'EOF'
import json, sys, os
path, raw, tag = sys.argv[1:4]
feats = json.load(open(path))["features"]
# one item per tile (keep the lowest cloud cover if a tile appears twice)
best = {}
for f in feats:
    t = f["properties"]["s2:mgrs_tile"]
    if t not in best or f["properties"]["eo:cloud_cover"] < best[t]["properties"]["eo:cloud_cover"]:
        best[t] = f
baselines = {f["properties"]["s2:processing_baseline"] for f in best.values()}
open(f"{raw}/offset_{tag}.txt", "w").write("1000\n" if max(float(b) for b in baselines) >= 4.0 else "0\n")
for band in ("B02", "B03", "B04", "B08", "B11"):
    with open(f"{raw}/s2_{tag}_{band}.txt", "w") as out:
        for f in best.values():
            out.write(f"/vsicurl/{f['assets'][band]['href']}?{os.environ['TOK']}\n")
print(tag, "tiles:", sorted(best), "baselines:", sorted(baselines))
EOF
  OFF=$(cat "$RAW/offset_$tag.txt")
  for band in B02 B03 B04 B08 B11; do
    gdalbuildvrt -q -overwrite -srcnodata 0 -input_file_list "$RAW/s2_${tag}_${band}.txt" "$RAW/s2_${tag}_${band}.vrt"
    # crop on the native grid; subtract the offset (slope 1) into Int16
    gdalwarp -q -overwrite -te $TE -tr 10 10 -r near -ot Int16 "$RAW/s2_${tag}_${band}.vrt" "$RAW/crop_${tag}_${band}.tif"
    gdal_translate -q -scale 0 10000 $((0-OFF)) $((10000-OFF)) -ot Int16 -a_nodata none "$RAW/crop_${tag}_${band}.tif" "$RAW/h_${tag}_${band}.tif"
  done
  gdalbuildvrt -q -overwrite -separate "$RAW/rgb_$tag.vrt" "$RAW/h_${tag}_B04.tif" "$RAW/h_${tag}_B03.tif" "$RAW/h_${tag}_B02.tif"
  gdal_translate -q $CO "$RAW/rgb_$tag.vrt" "$OUT/Zomba_Sentinel2_RGB_$tag.tif"
  gdal_translate -q $CO "$RAW/h_${tag}_B08.tif" "$OUT/Zomba_Sentinel2_NIR_$tag.tif"
  gdal_translate -q $CO "$RAW/h_${tag}_B11.tif" "$OUT/Zomba_Sentinel2_SWIR_$tag.tif"
  echo "$tag done (offset removed: $OFF)"
done

# ---- built-up surface, 2015 and 2025 (GHSL) ---------------------------------------------------
# Sentinel-2 alone can't measure built-up growth here: both dates are dry season, when bare soil
# reflects like rooftops (a built-up index flags ~80% of this square, of which ~4% is really
# built-up). So the measuring is done on the JRC Global Human Settlement built-up surface layer,
# which is modelled from imagery for fixed epochs. Values are m2 of built-up surface per 100 m
# cell (0-10000). Tile R11_C22 covers Zomba. Licence: CC BY 4.0, European Commission JRC.
# Epochs 2015 and 2020 only: JRC produces 2025 and 2030 as projections, and this project should
# measure change that was observed, not modelled forward.
GHSL=https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A
for epoch in 2015 2020; do
  name="GHS_BUILT_S_E${epoch}_GLOBE_R2023A_54009_100_V1_0_R11_C22"
  zip="$RAW/$name.zip"
  [ -s "$zip" ] || curl -fsSL --retry 5 -o "$zip" \
    "$GHSL/GHS_BUILT_S_E${epoch}_GLOBE_R2023A_54009_100/V1-0/tiles/$name.zip"
  gdalwarp -q -overwrite -te $TE -tr 100 100 -r bilinear -t_srs EPSG:32736 \
    -of GTiff -co COMPRESS=DEFLATE -co TILED=YES \
    "/vsizip/$zip/$name.tif" "$OUT/Zomba_builtup_${epoch}_GHSL.tif"
  echo "built-up $epoch done"
done

ls -la "$OUT"
