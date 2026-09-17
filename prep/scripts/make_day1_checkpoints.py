#!/usr/bin/env python3
"""Build the four Exercise 1 checkpoints for Day 1 (Nsanje flood).

Writes day1_floods/checkpoints/:
  day1_stage_A.qgz  QGIS opened on the flood data: colour image, districts, the NIR band
  day1_stage_B.qgz  plus the before/after water layers from the < 10000 threshold
  day1_stage_C.qgz  plus the Sentinel-1 radar image and its own water layer (the SAR extension)
  day1_stage_D.qgz  plus flood polygons, buildings, and the 108 flooded buildings

Layers use relative paths (../activity/... and ./data/...), so a checkpoint works from a copy of
the day1_floods folder. Run prep/scripts/make_day1_checkpoints.py after changing any styling.
The intermediate files in checkpoints/data are produced by the Stage B/C/D steps themselves.
"""
import os
import re
import subprocess
import uuid
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DAY1 = os.path.join(ROOT, "day1_floods")
CKPT = os.path.join(DAY1, "checkpoints")
TEMPLATE = os.path.join(ROOT, "day3_projects", "project4_chikwawa_flood",
                        "checkpoints", "project_4_checkpoint_1.qgz")

def crs_block():
    with zipfile.ZipFile(TEMPLATE) as z:
        qgs = z.read([n for n in z.namelist() if n.endswith(".qgs")][0]).decode("utf-8")
    return re.search(r"<spatialrefsys.*?</spatialrefsys>", qgs, re.S).group(0)

CRS = crs_block()
WKT4326 = 'GEOGCS["WGS 84",    DATUM["WGS_1984",        SPHEROID["WGS 84",6378137,298.257223563,            AUTHORITY["EPSG","7030"]],        AUTHORITY["EPSG","6326"]],    PRIMEM["Greenwich",0,        AUTHORITY["EPSG","8901"]],    UNIT["degree",0.0174532925199433,        AUTHORITY["EPSG","9122"]],    AXIS["Latitude",NORTH],    AXIS["Longitude",EAST],    AUTHORITY["EPSG","4326"]]'
PROJ4_4326 = '+proj=longlat +datum=WGS84 +no_defs'

def path_of(rel):
    return os.path.join(DAY1, rel.replace("../", "").replace("./", "checkpoints/"))

def raster_extent(rel):
    out = subprocess.run(["gdalinfo", path_of(rel)], capture_output=True, text=True).stdout
    ul = re.search(r"Upper Left\s+\(\s*([-\d.]+),\s*([-\d.]+)\)", out)
    lr = re.search(r"Lower Right\s+\(\s*([-\d.]+),\s*([-\d.]+)\)", out)
    return float(ul.group(1)), float(lr.group(2)), float(lr.group(1)), float(ul.group(2))

def vector_extent(rel, layer=None):
    cmd = ["ogrinfo", "-so", "-al", path_of(rel)] if layer is None else \
          ["ogrinfo", "-so", path_of(rel), layer]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.search(r"Extent: \(([-\d.]+), ([-\d.]+)\) - \(([-\d.]+), ([-\d.]+)\)", out)
    return tuple(float(g) for g in m.groups())

def extent_xml(e):
    return ("<extent><xmin>%.6f</xmin><ymin>%.6f</ymin><xmax>%.6f</xmax><ymax>%.6f</ymax></extent>"
            % e)

# ------------------------------------------------------------------ renderers
def rgb(minv, maxv):
    band = ('<%sContrastEnhancement><minValue>%s</minValue><maxValue>%s</maxValue>'
            '<algorithm>StretchToMinimumMaximum</algorithm></%sContrastEnhancement>')
    return ('<rasterrenderer type="multibandcolor" band="1" redBand="1" greenBand="2" blueBand="3" '
            'opacity="1" alphaBand="-1" nodataColor="">'
            + band % ("red", minv, maxv, "red")
            + band % ("green", minv, maxv, "green")
            + band % ("blue", minv, maxv, "blue")
            + '</rasterrenderer>')

def gray(minv, maxv):
    return ('<rasterrenderer type="singlebandgray" band="1" opacity="1" alphaBand="-1" '
            'gradient="BlackToWhite" nodataColor="">'
            '<contrastEnhancement><minValue>%s</minValue><maxValue>%s</maxValue>'
            '<algorithm>StretchToMinimumMaximum</algorithm></contrastEnhancement>'
            '</rasterrenderer>' % (minv, maxv))

def mask(colour, label):
    """Value 1 in colour, everything else (0) left out of the palette, so it draws transparent."""
    return ('<rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">'
            f'<colorPalette><paletteEntry value="1" color="{colour}" alpha="255" label="{label}"/>'
            '</colorPalette></rasterrenderer>')

def raster_layer(rel, name, renderer):
    e = raster_extent(rel)
    lid = re.sub(r"\W", "_", name) + "_" + uuid.uuid4().hex
    xml = ('<maplayer type="raster" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" '
           'autoRefreshMode="Disabled" refreshOnNotifyEnabled="0">'
           f'<id>{lid}</id><datasource>{rel}</datasource><layername>{name}</layername>'
           f'<provider>gdal</provider><srs>{CRS}</srs>{extent_xml(e)}'
           f'<pipe>{renderer}<brightnesscontrast brightness="0" contrast="0" gamma="1"/>'
           '<huesaturation saturation="0" grayscaleMode="0" colorizeOn="0"/>'
           '<rasterresampler maxOversampling="2"/></pipe><blendMode>0</blendMode></maplayer>')
    return lid, xml, name

def srs_block(epsg):
    """The districts ship in EPSG:4326 (Stage A step 6 compares layer CRS with project CRS)."""
    if epsg == 32736:
        return CRS
    # QGIS needs a full definition here; an authid on its own loads but will not draw
    return ("""<spatialrefsys nativeFormat="Wkt"><wkt>%s</wkt><proj4>%s</proj4>"""
            """<srsid>3452</srsid><srid>4326</srid><authid>EPSG:4326</authid>"""
            """<description>WGS 84</description><projectionacronym>longlat</projectionacronym>"""
            """<ellipsoidacronym>EPSG:7030</ellipsoidacronym>"""
            """<geographicflag>true</geographicflag></spatialrefsys>""") % (WKT4326, PROJ4_4326)

def vector_layer(rel, name, symbol, geom, layer_in_file=None, epsg=32736, wkb=None):
    e = vector_extent(rel, layer_in_file)
    lid = re.sub(r"\W", "_", name) + "_" + uuid.uuid4().hex
    src = rel + (f"|layername={layer_in_file}" if layer_in_file else "")
    xml = ('<maplayer type="vector" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" '
           f'geometry="{geom}" wkbType="{wkb or geom}" autoRefreshMode="Disabled" refreshOnNotifyEnabled="0" '
           'simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" '
           'simplifyAlgorithm="0" readOnly="0" labelsEnabled="0" symbologyReferenceScale="-1">'
           f'<id>{lid}</id><datasource>{src}</datasource><layername>{name}</layername>'
           f'<provider encoding="UTF-8">ogr</provider><srs>{srs_block(epsg)}</srs>{extent_xml(e)}'
           '<renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0" '
           f'referencescale="-1"><symbols>{symbol}</symbols></renderer-v2>'
           '<blendMode>0</blendMode><featureBlendMode>0</featureBlendMode></maplayer>')
    return lid, xml, name

def fill(stroke, width, style="no", colour="0,0,0,0"):
    return ('<symbol type="fill" name="0" alpha="1" clip_to_extent="1" force_rhr="0" '
            'frame_rate="10" is_animated="0">'
            f'<layer class="SimpleFill" enabled="1" pass="0" locked="0" id="{{{uuid.uuid4()}}}">'
            '<Option type="Map">'
            f'<Option name="color" type="QString" value="{colour}"/>'
            f'<Option name="style" type="QString" value="{style}"/>'
            f'<Option name="outline_color" type="QString" value="{stroke}"/>'
            f'<Option name="outline_width" type="QString" value="{width}"/>'
            '<Option name="outline_width_unit" type="QString" value="MM"/>'
            '<Option name="outline_style" type="QString" value="solid"/>'
            '<Option name="joinstyle" type="QString" value="bevel"/>'
            '</Option></layer></symbol>')

def centroid_dots(colour, size):
    """One dot per polygon: buildings are ~4 m across, invisible at district zoom."""
    return ('<symbol type="fill" name="0" alpha="1" clip_to_extent="1" force_rhr="0" '
            'frame_rate="10" is_animated="0">'
            f'<layer class="CentroidFill" enabled="1" pass="0" locked="0" id="{{{uuid.uuid4()}}}">'
            '<Option type="Map">'
            '<Option name="clip_on_current_part_only" type="QString" value="0"/>'
            '<Option name="clip_points" type="QString" value="0"/>'
            '<Option name="point_on_all_parts" type="QString" value="1"/>'
            '<Option name="point_on_surface" type="QString" value="0"/></Option>'
            '<symbol type="marker" name="@0@0" alpha="1" clip_to_extent="1" force_rhr="0" '
            'frame_rate="10" is_animated="0">'
            f'<layer class="SimpleMarker" enabled="1" pass="0" locked="0" id="{{{uuid.uuid4()}}}">'
            '<Option type="Map">'
            '<Option name="name" type="QString" value="circle"/>'
            f'<Option name="color" type="QString" value="{colour}"/>'
            f'<Option name="size" type="QString" value="{size}"/>'
            '<Option name="size_unit" type="QString" value="MM"/>'
            '<Option name="outline_color" type="QString" value="35,35,35,255"/>'
            '<Option name="outline_width" type="QString" value="0.2"/>'
            '<Option name="outline_width_unit" type="QString" value="MM"/>'
            '<Option name="outline_style" type="QString" value="solid"/>'
            '<Option name="angle" type="QString" value="0"/>'
            '<Option name="offset" type="QString" value="0,0"/>'
            '<Option name="scale_method" type="QString" value="diameter"/>'
            '</Option></layer></symbol></layer></symbol>')

# ------------------------------------------------------------------ the stages
DISTRICTS = ("../activity/gadm41_MWI_1.shp", "gadm41_MWI_1",
             fill("255,220,0,255", "0.6"), "Polygon", None, 4326)

def stage_layers(stage):
    """Top to bottom, as the Layers panel should read at the end of each stage."""
    L = []
    if stage >= 4:
        L += [vector_layer("./data/flooded_buildings.gpkg", "flooded_buildings",
                           centroid_dots("235,45,45,255", "3"), "Polygon", "flooded_buildings", 32736, "MultiPolygon"),
              vector_layer("../activity/nsanje_buildings.shp", "nsanje_buildings",
                           fill("110,110,110,255", "0.2", "solid", "220,220,220,140"), "Polygon"),
              vector_layer("./data/water_postflood_shapes.gpkg", "water_postflood_shapes",
                           fill("20,90,200,255", "0.2", "solid", "60,130,230,150"),
                           "Polygon", "water_postflood_shapes", 32736, "MultiPolygon")]
    if stage == 3:
        L += [raster_layer("./data/sar_water_postflood.tif", "SAR water (post-flood)",
                           mask("#ff7f00", "water (radar)")),
              raster_layer("./data/water_postflood.tif", "water_postflood",
                           mask("#1f78b4", "water (NIR)")),
              raster_layer("../activity/Nsanje_Sentinel1_VV_dB_postflood.tif",
                           "Sentinel-1 VV dB (post-flood)", gray(-25, 5))]
    if stage == 2:
        L += [raster_layer("./data/water_postflood.tif", "water_postflood",
                           mask("#1f78b4", "water (post-flood)")),
              raster_layer("./data/water_preflood.tif", "water_preflood",
                           mask("#a6cee3", "water (pre-flood)"))]
    L.append(vector_layer(*DISTRICTS))
    if stage == 2:
        L += [raster_layer("../activity/Nsanje_Landsat8_NIR_postflood.tif",
                           "Nsanje_Landsat8_NIR_postflood", gray(6700, 26000))]
    if stage in (1, 2):
        L += [raster_layer("../activity/Nsanje_Landsat8_NIR_preflood.tif",
                           "Nsanje_Landsat8_NIR_preflood", gray(7000, 26000))]
    img = "postflood" if stage >= 3 else "preflood"
    L.append(raster_layer(f"../activity/Nsanje_Landsat8_RGB_{img}.tif",
                          f"Nsanje_Landsat8_RGB_{img}", rgb(7000, 16000)))
    return L

def write(stage, out_name, title):
    layers = stage_layers(stage)
    tree = "".join('<layer-tree-layer id="%s" name="%s" source="%s" providerKey="%s" '
                   'checked="Qt::Checked" expanded="0"><customproperties/></layer-tree-layer>'
                   % (lid, name, re.search(r"<datasource>(.*?)</datasource>", xml).group(1),
                      "gdal" if 'type="raster"' in xml else "ogr")
                   for lid, xml, name in layers)
    canvas = raster_extent("../activity/Nsanje_Landsat8_RGB_preflood.tif")
    qgs = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<qgis projectname="{title}" version="3.44.14-Solothurn">'
           f'<homePath path=""/><title>{title}</title><projectCrs>{CRS}</projectCrs>'
           f'<layer-tree-group>{tree}<custom-order enabled="0">'
           + "".join("<item>%s</item>" % lid for lid, _, _ in layers) +
           '</custom-order></layer-tree-group>'
           '<mapcanvas name="theMapCanvas" annotationsVisible="1"><units>meters</units>'
           f'{extent_xml(canvas)}<rotation>0</rotation><destinationsrs>{CRS}</destinationsrs>'
           '</mapcanvas>'
           '<projectlayers>' + "".join(xml for _, xml, _ in layers) + '</projectlayers>'
           '<layerorder>' + "".join('<layer id="%s"/>' % lid for lid, _, _ in layers) + '</layerorder>'
           '<properties><Measure><Ellipsoid type="QString">WGS84</Ellipsoid></Measure></properties>'
           '</qgis>')
    os.makedirs(CKPT, exist_ok=True)
    with zipfile.ZipFile(os.path.join(CKPT, out_name), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(out_name.replace(".qgz", ".qgs"), qgs)
    print("wrote %s (%d layers)" % (out_name, len(layers)))

if __name__ == "__main__":
    write(1, "day1_stage_A.qgz", "Day 1 - end of Stage A")
    write(2, "day1_stage_B.qgz", "Day 1 - end of Stage B")
    write(3, "day1_stage_C.qgz", "Day 1 - end of Stage C (SAR)")
    write(4, "day1_stage_D.qgz", "Day 1 - end of Stage D")
