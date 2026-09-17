#!/usr/bin/env bash
# Clip EOG annual VIIRS night lights (VNL) to Malawi and reproject to EPSG:32736.
# Input: the global "average_masked" files, downloaded by hand from eogdata.mines.edu (EOG only
# allows browser downloads on free accounts), placed in data_library/_raw/viirs/.
#   2012 (Apr–Dec only) to 2021: VNL V2.1, Suomi NPP
#   2022: VNL V2.2, Suomi NPP + NOAA-20 — different processing version, so treat 2021→2022 with care
# License: CC BY 4.0. Cite EOG and Elvidge et al. (2021), Remote Sensing 13(5):922.
# Units: nW/cm²/sr. Masked = fires, ephemeral lights and unlit background set to zero.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RAW="$ROOT/data_library/_raw/viirs"
OUT="$ROOT/data_library/nightlights"
mkdir -p "$OUT"

for f in "$RAW"/VNL_v2*average_masked.dat.tif.gz; do
  name=$(basename "$f")
  case "$name" in *"(1)"*) continue ;; esac                       # browser duplicate
  ver=$(echo "$name" | sed -E 's/^VNL_(v2[0-9])_.*/\1/')
  period=$(echo "$name" | sed -E 's/^VNL_v2[0-9]_[a-z0-9-]+_([0-9-]+)_global.*/\1/')
  out="$OUT/viirs_vnl_${ver}_${period}_average_masked_MWI.tif"
  [ -s "$out" ] && { echo "skip $period"; continue; }
  echo "$period ($ver)"
  # Native grid is 15 arc-seconds (~460 m here). Nearest neighbor keeps each lit cell's radiance.
  gdalwarp -q -te_srs EPSG:4326 -te 32.55 -17.25 36.05 -9.25 -t_srs EPSG:32736 -tr 460 460 -r near \
    -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=3 -co TILED=YES "/vsigzip/$f" "$out.part"
  mv "$out.part" "$out"
done
ls -la "$OUT"
