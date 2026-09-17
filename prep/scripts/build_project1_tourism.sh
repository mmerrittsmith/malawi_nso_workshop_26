#!/bin/bash
# Mini-project 1 data: tourism tour of eight places in Malawi.
# Vectors from the OSM extract in data_library; rasters copied from data_library; Sentinel-2
# pictures of the eight stops for August 2016 and September 2025 (Planetary Computer).
# Stops are 6 km circles (3 km radius) listed in day3_projects/project1_tourism/stops.csv.
#
# The two Sentinel-2 files are sparse mosaics: full-country grid, pixels only at the eight stops.
# They are 8-bit color, stretched the same way as the Malawi basemap (150–1800 reflectance x10000),
# with the +1000 offset removed from 2022-and-later scenes first, so 2016 and 2025 look comparable.
set -euo pipefail
export GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR GDAL_HTTP_MAX_RETRY=5 GDAL_HTTP_RETRY_DELAY=5
export GDAL_HTTP_TIMEOUT=120 GDAL_HTTP_CONNECTTIMEOUT=30 CPL_VSIL_CURL_CHUNK_SIZE=1048576

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/day3_projects/project1_tourism"
LIB="$ROOT/data_library"
OSM="$LIB/osm"
RAW="$LIB/_raw/project1"
mkdir -p "$OUT" "$RAW"
cd "$OUT"
# same layout as project 4: data at the top, checkpoints/outputs/screenshots beside it
mkdir -p checkpoints/data outputs screenshots

# ---- stops, accommodation, buildings, protected areas ---------------------------------------
ogr2ogr -f GPKG -overwrite -a_srs EPSG:4326 -oo X_POSSIBLE_NAMES=lon -oo Y_POSSIBLE_NAMES=lat \
  -oo AUTODETECT_TYPE=YES "$RAW/stop_points.gpkg" stops.csv -nln stops
ogr2ogr -f GPKG -overwrite tour_stops.gpkg "$RAW/stop_points.gpkg" -nln tour_stops -a_srs EPSG:32736 \
  -dialect sqlite -sql "SELECT CAST(stop AS INTEGER) AS stop, name, ST_Buffer(ST_Transform(geom,32736),3000) AS geom FROM stops ORDER BY stop"

ogr2ogr -f GPKG -overwrite accommodation.gpkg "$OSM/gis_osm_pois_free_1.shp" -nln accommodation \
  -where "fclass IN ('hotel','guesthouse','hostel','motel','camp_site','caravan_site','chalet','alpine_hut')" \
  -select osm_id,name,fclass
ogr2ogr -f GPKG -update -append accommodation.gpkg "$OSM/gis_osm_pois_a_free_1.shp" -nln accommodation \
  -dialect sqlite -sql "SELECT osm_id, name, fclass, ST_Centroid(geometry) AS geom FROM gis_osm_pois_a_free_1 WHERE fclass IN ('hotel','guesthouse','hostel','motel','camp_site','caravan_site','chalet')"

ogr2ogr -f GPKG -overwrite osm_buildings_stops.gpkg "$OSM/gis_osm_buildings_a_free_1.shp" \
  -nln osm_buildings_stops -clipsrc tour_stops.gpkg -select osm_id,name,type

# Geofabrik's protected areas have no names; label the two the tour visits by which one contains the stop
ogr2ogr -f "ESRI Shapefile" -overwrite protected_areas.shp "$OSM/gis_osm_protected_areas_a_free_1.shp" \
  -dialect sqlite -sql "SELECT osm_id, fclass,
    CASE WHEN ST_Intersects(geometry, ST_Transform(MakePoint(34.0503,-12.9112,4326),32736)) THEN 'Nkhotakota Wildlife Reserve'
         WHEN ST_Intersects(geometry, ST_Transform(MakePoint(35.2948,-14.8501,4326),32736)) THEN 'Liwonde National Park'
         ELSE '' END AS name, geometry FROM gis_osm_protected_areas_a_free_1"

# ---- rasters copied from the library ---------------------------------------------------------
cp -f "$LIB/imagery/malawi_s2_rgb_2021_30m.tif" .
cp -f "$LIB/landcover/ESA_WorldCover_10m_2021_v200_MWI.tif" .
cp -f "$LIB/population/mwi_pop_2025_CN_100m_R2025A_v1.tif" .
cp -f "$LIB/nightlights/viirs_vnl_v21_2014_average_masked_MWI.tif" .
cp -f "$LIB/nightlights/viirs_vnl_v21_2021_average_masked_MWI.tif" .

# ---- Sentinel-2 pictures of the eight stops ---------------------------------------------------
TOK=$(curl -sS -m 60 https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-2-l2a | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
build_year() {  # build_year LABEL WINDOW
  local label=$1 window=$2
  : > "$RAW/tiles_$label.txt"
  tail -n +2 stops.csv | while IFS=, read -r stop name lon lat; do
    local box; box=$(TOK="$TOK" python3 - "$lon" "$lat" "$window" "$RAW/bands_${label}_${stop}" <<'PY'
import json, sys, os, urllib.request
lon, lat, window, prefix = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4]
body = json.dumps({"collections": ["sentinel-2-l2a"], "bbox": [lon-0.04, lat-0.04, lon+0.04, lat+0.04],
                   "datetime": window, "limit": 50, "query": {"eo:cloud_cover": {"lt": 20}}}).encode()
req = urllib.request.Request("https://planetarycomputer.microsoft.com/api/stac/v1/search", data=body,
                             headers={"Content-Type": "application/json"})
feats = None
for attempt in range(5):        # the search endpoint fails intermittently
    try:
        feats = json.load(urllib.request.urlopen(req, timeout=120))["features"]
        break
    except Exception as exc:
        if attempt == 4:
            raise
        import time; time.sleep(5 * (attempt + 1))
feats.sort(key=lambda f: f["properties"]["eo:cloud_cover"])
best_day = feats[0]["properties"]["datetime"][:10]
# one Sentinel-2 tile may not cover the whole circle. Take every scene from the best day, and
# put the next-best days underneath as filler so there are no holes. gdalbuildvrt draws later
# files on top, so the chosen day is written last.
same_day = [f for f in feats if f["properties"]["datetime"][:10] == best_day]
other_days = [f for f in feats if f["properties"]["datetime"][:10] != best_day][:6]
ordered = list(reversed(other_days)) + same_day
tok = os.environ["TOK"]
for band in ("B04", "B03", "B02"):
    with open(f"{prefix}_{band}.txt", "w") as fh:
        for f in ordered:
            fh.write(f"/vsicurl/{f['assets'][band]['href']}?{tok}\n")
# offset: scenes processed with baseline 04.00+ carry +1000
off = 1000 if max(float(f["properties"]["s2:processing_baseline"]) for f in same_day) >= 4.0 else 0
print(best_day, off, len(same_day))
PY
)
    local date off scenes; date=$(echo "$box" | cut -d' ' -f1); off=$(echo "$box" | cut -d' ' -f2); scenes=$(echo "$box" | cut -d' ' -f3)
    # 6 km box around the stop, snapped to the 10 m grid
    read -r cx cy < <(echo "$lon $lat" | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:32736 | awk '{print $1, $2}')
    local x0 y0; x0=$(python3 -c "print(int(round(($cx-3000)/10))*10)"); y0=$(python3 -c "print(int(round(($cy-3000)/10))*10)")
    for band in B04 B03 B02; do
      gdalbuildvrt -q -overwrite -srcnodata 0 -input_file_list "$RAW/bands_${label}_${stop}_${band}.txt" "$RAW/s2_${label}_${stop}_${band}.vrt"
    done
    gdalbuildvrt -q -overwrite -separate "$RAW/s2_${label}_${stop}.vrt" \
      "$RAW/s2_${label}_${stop}_B04.vrt" "$RAW/s2_${label}_${stop}_B03.vrt" "$RAW/s2_${label}_${stop}_B02.vrt"
    gdalwarp -q -overwrite -t_srs EPSG:32736 -te $x0 $y0 $((x0+6000)) $((y0+6000)) -tr 10 10 -r near \
      "$RAW/s2_${label}_${stop}.vrt" "$RAW/s2_${label}_${stop}_raw.tif"
    gdal_translate -q -ot Byte -scale $((150+off)) $((1800+off)) 1 255 -a_nodata 0 \
      -co COMPRESS=DEFLATE -co TILED=YES "$RAW/s2_${label}_${stop}_raw.tif" "$RAW/s2_${label}_${stop}.tif"
    echo "$RAW/s2_${label}_${stop}.tif" >> "$RAW/tiles_$label.txt"
    local empty; empty=$(gdalinfo -stats "$RAW/s2_${label}_${stop}.tif" | grep -m1 STATISTICS_VALID_PERCENT | sed 's/.*=//')
    rm -f "$RAW/s2_${label}_${stop}.tif.aux.xml"
    echo "  stop $stop ($name): $date, $scenes scene(s), offset $off, valid ${empty}%"
  done
  gdalbuildvrt -q -overwrite -input_file_list "$RAW/tiles_$label.txt" "$RAW/mosaic_$label.vrt"
  gdal_translate -q -co COMPRESS=DEFLATE -co TILED=YES -co SPARSE_OK=TRUE -co BIGTIFF=IF_SAFER \
    -co PHOTOMETRIC=RGB "$RAW/mosaic_$label.vrt" "Sentinel2_$label.tif"
  gdaladdo -q -r average "Sentinel2_$label.tif" 2 4 8 16
  echo "Sentinel2_$label.tif done"
}
echo "August 2016:";    build_year 2016 "2016-08-01T00:00:00Z/2016-09-15T23:59:59Z"
echo "September 2025:"; build_year 2025 "2025-08-20T00:00:00Z/2025-10-15T23:59:59Z"

ls -la "$OUT"
