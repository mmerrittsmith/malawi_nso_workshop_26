#!/bin/bash
# Mini-project 4 data: the Day 1 flood workflow on Chikwawa, same flood as Nsanje.
# A 30 x 30 km square on the Shire floodplain (1008 x 1008 Landsat pixels, like the Nsanje files),
# chosen for the most new water and least cloud: 10.0 km² new water, 0.6% cloud post-flood.
#   Landsat 8 C2 L2 (Planetary Computer): pre 2024-09-19, post 2025-03-14 — near-infrared and RGB,
#     on Landsat's own pixel grid (nearest neighbor, no resampling), values as delivered (DN).
#   Sentinel-1 RTC VV (Planetary Computer), orbit 79 (covers the whole square): candidate dates
#     written to scratch; the pair used is picked after checking the water signal.
#   Buildings: Google Open Buildings v3, tile 18d, clipped by building centroid.
set -euo pipefail
export GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR GDAL_HTTP_MAX_RETRY=5 GDAL_HTTP_RETRY_DELAY=5

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/day3_projects/project4_chikwawa_flood"
RAW="$ROOT/data_library/_raw/project4"
mkdir -p "$OUT" "$RAW"
TE="691665 8175475 721905 8205715"          # xmin ymin xmax ymax, EPSG:32736, Landsat-aligned
LL="34.79 -16.50 35.08 -16.22"              # same square in lon/lat (slightly generous)
CO="-co COMPRESS=DEFLATE -co PREDICTOR=2 -co TILED=YES"
STAC=https://planetarycomputer.microsoft.com/api/stac/v1
token() { curl -sS -m 60 "https://planetarycomputer.microsoft.com/api/sas/v1/token/$1" | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])"; }
href() {  # href COLLECTION ITEM_ID ASSET TOKEN
  curl -sS -m 60 "$STAC/collections/$1/items/$2" | TOK="$4" python3 -c "import sys,json,os;print(json.load(sys.stdin)['assets']['$3']['href']+'?'+os.environ['TOK'])"
}

# ---- Landsat ------------------------------------------------------------------------------
LT=$(token landsat-c2-l2)
for pair in "20240919 preflood" "20250314 postflood"; do
  set -- $pair; d=$1; label=$2
  for band in nir08 red green blue; do
    : > "$RAW/l_${d}_${band}.txt"
    for row in 071 072; do
      echo "/vsicurl/$(href landsat-c2-l2 LC08_L2SP_167${row}_${d}_02_T1 $band "$LT")" >> "$RAW/l_${d}_${band}.txt"
    done
    gdalbuildvrt -q -overwrite -input_file_list "$RAW/l_${d}_${band}.txt" "$RAW/l_${d}_${band}.vrt"
  done
  gdalwarp -q -overwrite -t_srs EPSG:32736 -te $TE -tr 30 30 -r near $CO \
    "$RAW/l_${d}_nir08.vrt" "$OUT/Chikwawa_Landsat8_NIR_${label}.tif"
  gdalbuildvrt -q -overwrite -separate "$RAW/l_${d}_rgb.vrt" "$RAW/l_${d}_red.vrt" "$RAW/l_${d}_green.vrt" "$RAW/l_${d}_blue.vrt"
  gdalwarp -q -overwrite -t_srs EPSG:32736 -te $TE -tr 30 30 -r near $CO \
    "$RAW/l_${d}_rgb.vrt" "$OUT/Chikwawa_Landsat8_RGB_${label}.tif"
  echo "Landsat $label done"
done

# ---- Sentinel-1 candidates (orbit 79) -------------------------------------------------------
ST=$(token sentinel-1-rtc)
curl -sS -m 60 -X POST "$STAC/search" -H 'Content-Type: application/json' \
  -d '{"collections":["sentinel-1-rtc"],"bbox":[34.79,-16.50,35.08,-16.22],"datetime":"2024-09-05T00:00:00Z/2025-03-25T23:59:59Z","limit":200}' \
  | python3 -c "
import sys,json
for f in json.load(sys.stdin)['features']:
    p=f['properties']; d=f['id'].split('_')[4][:8]
    if p['sat:relative_orbit']==79 and d in ('20240912','20240924','20250311','20250323'):
        print(d, f['assets']['vv']['href'])" > "$RAW/s1_items.txt"
for d in 20240912 20240924 20250311 20250323; do
  grep "^$d " "$RAW/s1_items.txt" | awk -v t="$ST" '{print "/vsicurl/" $2 "?" t}' > "$RAW/s1_$d.txt"
  gdalbuildvrt -q -overwrite -input_file_list "$RAW/s1_$d.txt" "$RAW/s1_$d.vrt"
  gdalwarp -q -overwrite -t_srs EPSG:32736 -te $TE -tr 10 10 -r bilinear -srcnodata -32768 -dstnodata -32768 \
    -co COMPRESS=DEFLATE -co TILED=YES "$RAW/s1_$d.vrt" "$RAW/s1_${d}_vv_linear.tif"
  echo "Sentinel-1 $d done"
done

# ---- Open Buildings -------------------------------------------------------------------------
OB="$RAW/18d_buildings.csv.gz"
[ -s "$OB" ] || curl -fsSL --retry 5 -o "$OB" https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/18d_buildings.csv.gz
set -- $LL
gzip -dc "$OB" | awk -F, -v x0=$1 -v y0=$2 -v x1=$3 -v y1=$4 \
  'NR==1 || ($2+0>=x0 && $2+0<=x1 && $1+0>=y0 && $1+0<=y1)' > "$RAW/chikwawa_buildings.csv"
ogr2ogr -overwrite -t_srs EPSG:32736 -s_srs EPSG:4326 -lco ENCODING=UTF-8 \
  -oo GEOM_POSSIBLE_NAMES=geometry -oo KEEP_GEOM_COLUMNS=NO -oo AUTODETECT_TYPE=YES \
  "$OUT/chikwawa_buildings.shp" "$RAW/chikwawa_buildings.csv"
# Spatial index (.qix) so QGIS joins run fast and don't warn about a missing index
/Applications/QGIS.app/Contents/MacOS/qgis_process run native:createspatialindex -- INPUT="$OUT/chikwawa_buildings.shp" >/dev/null
ogrinfo -so -al "$OUT/chikwawa_buildings.shp" | grep -E "Feature Count|Extent"
echo "all done"
