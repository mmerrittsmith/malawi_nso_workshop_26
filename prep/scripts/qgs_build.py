#!/usr/bin/env python3
"""Shared pieces for writing QGIS project files (.qgz) by hand.

Used by make_day1_checkpoints.py and make_project2_checkpoints.py. Set BASE["dir"] to the folder
the checkpoints sit under before calling anything, so relative paths resolve.

Two things that cost an afternoon to find out:
  * geometry= takes Point/Line/Polygon only. "MultiPolygon" there loads but never draws.
  * a layer whose CRS differs from the project needs a full <spatialrefsys>, not just an authid.
"""
import os
import re
import subprocess
import uuid
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEMPLATE = os.path.join(ROOT, "day3_projects", "project4_chikwawa_flood",
                        "checkpoints", "project_4_checkpoint_1.qgz")

def crs_block():
    with zipfile.ZipFile(TEMPLATE) as z:
        qgs = z.read([n for n in z.namelist() if n.endswith(".qgs")][0]).decode("utf-8")
    return re.search(r"<spatialrefsys.*?</spatialrefsys>", qgs, re.S).group(0)

CRS = crs_block()
WKT4326 = 'GEOGCS["WGS 84",    DATUM["WGS_1984",        SPHEROID["WGS 84",6378137,298.257223563,            AUTHORITY["EPSG","7030"]],        AUTHORITY["EPSG","6326"]],    PRIMEM["Greenwich",0,        AUTHORITY["EPSG","8901"]],    UNIT["degree",0.0174532925199433,        AUTHORITY["EPSG","9122"]],    AXIS["Latitude",NORTH],    AXIS["Longitude",EAST],    AUTHORITY["EPSG","4326"]]'
PROJ4_4326 = '+proj=longlat +datum=WGS84 +no_defs'

BASE = {"dir": None}          # set by the caller: the project folder the checkpoints live under

def path_of(rel):
    return os.path.join(BASE["dir"], rel.replace("../", "").replace("./", "checkpoints/"))

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

