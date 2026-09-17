#!/usr/bin/env bash
# Monthly NDVI for Malawi from NASA AppEEARS area-request output (MOD13A3.061, 1 km, Jan 2015 on).
# Input: the AppEEARS GeoTIFFs (NDVI + pixel_reliability layers), in data_library/_raw/ndvi/.
# Output: data_library/ndvi/mod13a3_ndvi_YYYY.MM_MWI.tif — real NDVI (−1 to 1), Float32,
#   EPSG:32736, 1 km. Pixels flagged cloudy (pixel reliability 3) or snow (2) are set to no data;
#   good (0) and marginal (1) are kept. Outside Malawi's outline is no data (AppEEARS masked it).
# Source: MOD13A3 v061, NASA LP DAAC, via AppEEARS. NASA data: no restrictions on reuse; cite
#   Didan, K. (2021). MODIS/Terra Vegetation Indices Monthly L3 Global 1km SIN Grid V061.
# Needs GDAL command-line tools and a Python with numpy (set PYTHON if not the default below).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RAW="$ROOT/data_library/_raw/ndvi"
OUT="$ROOT/data_library/ndvi"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
PYTHON="${PYTHON:-/Users/MMSMITH/miniconda3/bin/python}"
mkdir -p "$OUT"

for ndvi in "$RAW"/MOD13A3.061__1_km_monthly_NDVI_doy*_aid*.tif; do
  doy=$(basename "$ndvi" | sed -E 's/.*_doy([0-9]{7}).*/\1/')
  ym=$("$PYTHON" -c "import datetime as d; x=d.datetime.strptime('$doy','%Y%j'); print(x.strftime('%Y.%m'))")
  out="$OUT/mod13a3_ndvi_${ym}_MWI.tif"
  [ -s "$out" ] && continue
  rel="${ndvi/_NDVI_/_pixel_reliability_}"
  gdal_translate -q -of ENVI -ot Float32 "$ndvi" "$TMP/v.bin"
  gdal_translate -q -of ENVI -ot Int16 "$rel" "$TMP/r.bin"
  "$PYTHON" - "$TMP" <<'EOF'
import sys, numpy as np
t = sys.argv[1]
v = np.fromfile(f"{t}/v.bin", dtype=np.float32)
r = np.fromfile(f"{t}/r.bin", dtype=np.int16)
bad = (v == -3000) | ~np.isin(r, (0, 1))
out = np.where(bad, -9999, v * 1e-4).astype(np.float32)
out.tofile(f"{t}/v.bin")
EOF
  gdalwarp -q -overwrite -srcnodata -9999 -dstnodata -9999 -t_srs EPSG:32736 -tr 1000 1000 -r near \
    -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=3 -co TILED=YES "$TMP/v.bin" "$out"
  echo "$ym"
done
ls "$OUT" | wc -l
