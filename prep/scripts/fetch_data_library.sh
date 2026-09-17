#!/usr/bin/env bash
# Build the national Malawi data library and fetch the QGIS installer for the flash drives.
# Every layer ends up in EPSG:32736 (UTM 36S), clipped to Malawi's bounding box plus a small
# buffer. Safe to re-run: finished outputs are skipped.
#
# Needs GDAL/OGR command-line tools (gdalwarp, gdalbuildvrt, ogr2ogr), curl and unzip.
# Not covered here, because they need a login or a decision first: VIIRS night lights, NDVI,
# Open Buildings, and imagery scenes for specific project areas.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LIB="$ROOT/data_library"
RAW="$LIB/_raw"             # downloads before clipping; delete once the library is built
INST="$ROOT/installers"
GADM_SRC="$ROOT/../projects/malawi/gadm41_MWI_shp"
mkdir -p "$LIB" "$RAW" "$INST"

# Malawi is 32.69–35.92 E, 17.13–9.36 S. Buffer of ~0.1 degrees.
BBOX_LL="32.55 -17.25 36.05 -9.25"          # xmin ymin xmax ymax, EPSG:4326
CO="-co COMPRESS=DEFLATE -co TILED=YES -co BIGTIFF=IF_SAFER"

log() { printf '\n[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
fetch() {  # fetch URL DEST — resumable, skips if complete
  curl -fL --retry 5 --retry-delay 5 -C - -o "$2" "$1" || { rm -f "$2"; return 1; }
}

# ---------------------------------------------------------------------------------------
log "QGIS 3.44 LTR Windows installer"
QGIS=QGIS-OSGeo4W-3.44.14-1.msi
[ -s "$INST/$QGIS" ] || fetch "https://download.osgeo.org/qgis/windows/$QGIS" "$INST/$QGIS"
ls -la "$INST/$QGIS"

# ---------------------------------------------------------------------------------------
log "GADM 4.1 boundaries, levels 0–3"
mkdir -p "$LIB/boundaries"
for l in 0 1 2 3; do
  out="$LIB/boundaries/gadm41_MWI_$l.shp"
  [ -s "$out" ] || ogr2ogr -t_srs EPSG:32736 -lco ENCODING=UTF-8 "$out" "$GADM_SRC/gadm41_MWI_$l.shp"
done

# ---------------------------------------------------------------------------------------
log "OpenStreetMap extract (Geofabrik)"
mkdir -p "$LIB/osm"
OSMZIP="$RAW/malawi-latest-free.shp.zip"
[ -s "$OSMZIP" ] || fetch https://download.geofabrik.de/africa/malawi-latest-free.shp.zip "$OSMZIP"
mkdir -p "$RAW/osm" && unzip -oq "$OSMZIP" -d "$RAW/osm"
cp -f "$RAW/osm/README" "$LIB/osm/README_geofabrik.txt" 2>/dev/null || true
for shp in "$RAW"/osm/*.shp; do
  out="$LIB/osm/$(basename "$shp")"
  [ -s "$out" ] || ogr2ogr -t_srs EPSG:32736 -lco ENCODING=UTF-8 "$out" "$shp"
done

# ---------------------------------------------------------------------------------------
log "WorldPop population 2025, 100 m, constrained (R2025A)"
mkdir -p "$LIB/population"
WP=mwi_pop_2025_CN_100m_R2025A_v1.tif
[ -s "$RAW/$WP" ] || fetch "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/MWI/v1/100m/constrained/$WP" "$RAW/$WP"
# Counts, not densities: "sum" resampling keeps the national total intact when reprojecting.
[ -s "$LIB/population/$WP" ] || gdalwarp -q -t_srs EPSG:32736 -tr 100 100 -r sum $CO "$RAW/$WP" "$LIB/population/$WP"

# ---------------------------------------------------------------------------------------
log "ESA WorldCover 2021 land cover, 10 m"
mkdir -p "$LIB/landcover" "$RAW/worldcover"
for lat in S21 S18 S15 S12 S09; do for lon in E030 E033; do
  t="ESA_WorldCover_10m_2021_v200_${lat}${lon}_Map.tif"
  [ -s "$RAW/worldcover/$t" ] || fetch "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/$t" "$RAW/worldcover/$t" || echo "  (no tile $t)"
done; done
WC="$LIB/landcover/ESA_WorldCover_10m_2021_v200_MWI.tif"
if [ ! -s "$WC" ]; then
  gdalbuildvrt -q "$RAW/worldcover.vrt" "$RAW"/worldcover/*.tif
  gdalwarp -q -te_srs EPSG:4326 -te $BBOX_LL -t_srs EPSG:32736 -tr 10 10 -r near $CO \
    "$RAW/worldcover.vrt" "$WC"
fi

# ---------------------------------------------------------------------------------------
log "Copernicus DEM GLO-90 elevation"
mkdir -p "$LIB/elevation" "$RAW/dem90"
for la in $(seq 8 18); do for lo in 32 33 34 35 36; do
  n="Copernicus_DSM_COG_30_S$(printf %02d $la)_00_E0${lo}_00_DEM"
  [ -s "$RAW/dem90/$n.tif" ] || fetch "https://copernicus-dem-90m.s3.amazonaws.com/$n/$n.tif" "$RAW/dem90/$n.tif" 2>/dev/null || true
done; done
DEM="$LIB/elevation/copernicus_dem_glo90_MWI.tif"
if [ ! -s "$DEM" ]; then
  gdalbuildvrt -q "$RAW/dem90.vrt" "$RAW"/dem90/*.tif
  gdalwarp -q -te_srs EPSG:4326 -te $BBOX_LL -t_srs EPSG:32736 -tr 90 90 -r bilinear $CO \
    "$RAW/dem90.vrt" "$DEM"
fi

# ---------------------------------------------------------------------------------------
log "CHIRPS v3 monthly rainfall, Jan 2015 onwards (Africa tifs, read remotely and clipped)"
mkdir -p "$LIB/rainfall/chirps_monthly"
for y in $(seq 2015 2026); do for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
  f="chirps-v3.0.$y.$m.tif"; out="$LIB/rainfall/chirps_monthly/$f"
  [ -s "$out" ] && continue
  gdalwarp -q -te_srs EPSG:4326 -te $BBOX_LL -t_srs EPSG:32736 -tr 5000 5000 -r near $CO \
    "/vsicurl/https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/africa/tifs/$f" "$out" 2>/dev/null \
    || { rm -f "$out"; echo "  (not published yet: $f)"; }
done; done

# ---------------------------------------------------------------------------------------
log "Done"
du -sh "$INST" "$LIB"/* 2>/dev/null
