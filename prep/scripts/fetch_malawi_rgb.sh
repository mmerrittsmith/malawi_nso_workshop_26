#!/usr/bin/env bash
# Malawi-wide true-color basemap, 30 m, EPSG:32736, to sit under the Day 1 rasters.
# Source: ESA WorldCover 2021 Sentinel-2 cloudless annual composite (RGBNIR, 10 m, CC BY 4.0).
#   Attribution: "ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021)
#   processed by ESA WorldCover consortium"
# Step 1 (this script, slow): read red/green/blue remotely from the tile overviews and warp to a
# local 30 m UInt16 intermediate. Step 2 (fast, re-runnable): stretch to 8-bit and compress.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RAW="$ROOT/data_library/_raw"
OUT="$ROOT/data_library/imagery"
mkdir -p "$RAW" "$OUT"
export GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR GDAL_HTTP_MULTIRANGE=YES GDAL_HTTP_MERGE_CONSECUTIVE_RANGES=YES \
       GDAL_HTTP_MAX_RETRY=5 GDAL_HTTP_RETRY_DELAY=5 VSI_CACHE=TRUE GDAL_CACHEMAX=2048

BASE=https://esa-worldcover-s2.s3.eu-central-1.amazonaws.com/rgbnir/2021
LIST="$RAW/worldcover_rgb_tiles.txt"; : > "$LIST"
for la in 10 11 12 13 14 15 16 17 18; do for lo in 032 033 034 035; do
  echo "/vsicurl/$BASE/S$la/ESA_WorldCover_10m_2021_v200_S${la}E${lo}_S2RGBNIR.tif" >> "$LIST"
done; done

MID="$RAW/malawi_s2_rgb_2021_30m_uint16.tif"
if [ ! -s "$MID" ]; then
  gdalbuildvrt -q -b 1 -b 2 -b 3 -input_file_list "$LIST" "$RAW/worldcover_rgb.vrt"
  gdalwarp -overwrite -multi -wo NUM_THREADS=ALL_CPUS -te_srs EPSG:4326 -te 32.55 -17.25 36.0 -9.25 \
    -t_srs EPSG:32736 -tr 30 30 -r average -srcnodata 0 -dstnodata 0 \
    -of GTiff -co COMPRESS=DEFLATE -co PREDICTOR=2 -co TILED=YES -co BIGTIFF=IF_SAFER \
    "$RAW/worldcover_rgb.vrt" "$MID.part" && mv "$MID.part" "$MID"
fi
gdalinfo "$MID" | grep -E "Size is|Pixel Size"
echo "intermediate done"

# Step 2: 8-bit true color. One linear stretch shared by all three bands (reflectance x10000,
# 150–1800 → 1–255) keeps the color balance natural; chosen by eye from previews. JPEG/YCbCr
# with an internal nodata mask keeps it small, and internal overviews keep QGIS fast when zoomed out.
FINAL="$OUT/malawi_s2_rgb_2021_30m.tif"
export GDAL_TIFF_INTERNAL_MASK=YES
# No nodata value on the output: JPEG can round dark lake pixels to 0, so gaps come from the mask.
gdal_translate -q -ot Byte -scale 150 1800 1 255 -mask 1 -colorinterp red,green,blue \
  -a_scale 1 -a_offset 0 -a_nodata none \
  -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=YCBCR -co TILED=YES -co BIGTIFF=IF_SAFER \
  "$MID" "$FINAL"
gdaladdo -q -r average --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR \
  --config INTERLEAVE_OVERVIEW PIXEL --config JPEG_QUALITY_OVERVIEW 85 "$FINAL" 2 4 8 16 32 64
ls -la "$FINAL"
