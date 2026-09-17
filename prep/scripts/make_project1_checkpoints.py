#!/usr/bin/env python3
"""Build the three Part 1 checkpoints for mini-project 1 (tourism).

Writes day3_projects/project1_tourism/checkpoints/:
  project1_checkpoint_1.qgz  after step 1.4  - the three pictures, ordered and renamed
  project1_checkpoint_2.qgz  after step 1.7  - plus land cover, lights and population, styled
  project1_start.qgz         after step 1.9  - everything, ordered: Part 1 finished

Layer paths are relative (../file), so a checkpoint works from a copy of the project folder.
The CRS block is lifted from a project 4 checkpoint so it matches what QGIS itself writes.
"""
import os
import re
import subprocess
import uuid
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROJ = os.path.join(ROOT, "day3_projects", "project1_tourism")
CKPT = os.path.join(PROJ, "checkpoints")
TEMPLATE_QGZ = os.path.join(ROOT, "day3_projects", "project4_chikwawa_flood",
                            "checkpoints", "project_4_checkpoint_1.qgz")

def crs_block():
    with zipfile.ZipFile(TEMPLATE_QGZ) as z:
        qgs = z.read([n for n in z.namelist() if n.endswith(".qgs")][0]).decode("utf-8")
    return re.search(r"<spatialrefsys.*?</spatialrefsys>", qgs, re.S).group(0)

CRS = crs_block()

def raster_extent(path):
    out = subprocess.run(["gdalinfo", path], capture_output=True, text=True).stdout
    ul = re.search(r"Upper Left\s+\(\s*([-\d.]+),\s*([-\d.]+)\)", out)
    lr = re.search(r"Lower Right\s+\(\s*([-\d.]+),\s*([-\d.]+)\)", out)
    x0, y1 = float(ul.group(1)), float(ul.group(2))
    x1, y0 = float(lr.group(1)), float(lr.group(2))
    return x0, y0, x1, y1

def vector_extent(path, layer=None):
    cmd = ["ogrinfo", "-so", "-al", path] if layer is None else ["ogrinfo", "-so", path, layer]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.search(r"Extent: \(([-\d.]+), ([-\d.]+)\) - \(([-\d.]+), ([-\d.]+)\)", out)
    return tuple(float(g) for g in m.groups())

def extent_xml(e):
    return ("<extent><xmin>%.6f</xmin><ymin>%.6f</ymin><xmax>%.6f</xmax><ymax>%.6f</ymax></extent>"
            % (e[0], e[1], e[2], e[3]))

# ---------------------------------------------------------------- renderers
def rgb_renderer():
    return ('<rasterrenderer type="multibandcolor" band="1" redBand="1" greenBand="2" blueBand="3" '
            'opacity="1" alphaBand="-1" nodataColor="">'
            '<redContrastEnhancement><minValue>1</minValue><maxValue>255</maxValue>'
            '<algorithm>StretchToMinimumMaximum</algorithm></redContrastEnhancement>'
            '<greenContrastEnhancement><minValue>1</minValue><maxValue>255</maxValue>'
            '<algorithm>StretchToMinimumMaximum</algorithm></greenContrastEnhancement>'
            '<blueContrastEnhancement><minValue>1</minValue><maxValue>255</maxValue>'
            '<algorithm>StretchToMinimumMaximum</algorithm></blueContrastEnhancement>'
            '</rasterrenderer>')

def paletted_builtup():
    # ESA WorldCover: keep only class 50 (built-up). Everything else draws transparent.
    return ('<rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">'
            '<colorPalette>'
            '<paletteEntry value="50" color="#e31a1c" alpha="255" label="Built-up"/>'
            '</colorPalette></rasterrenderer>')

def pseudocolor(vmin, vmax, stops):
    # first stop is fully transparent, so unlit/empty ground shows the picture underneath
    # (same effect as the handout's Transparency > Additional no data value = 0)
    items = "".join('<item value="%s" color="%s" alpha="%d" label="%s"/>'
                    % (v, c, 0 if i == 0 else 255, ("%g" % v))
                    for i, (v, c) in enumerate(stops))
    return ('<rasterrenderer type="singlebandpseudocolor" band="1" opacity="1" alphaBand="-1" '
            'classificationMin="%s" classificationMax="%s" nodataColor="">'
            '<rastershader><colorrampshader colorRampType="INTERPOLATED" classificationMode="1" '
            'clip="0" minimumValue="%s" maximumValue="%s" labelPrecision="2">%s</colorrampshader>'
            '</rastershader></rasterrenderer>' % (vmin, vmax, vmin, vmax, items))

MAGMA = [(0, "#000004"), (1.25, "#51127c"), (2.5, "#b73779"), (3.75, "#fc8961"), (5, "#fcfdbf")]
BLUES = [(0, "#f7fbff"), (12.5, "#c6dbef"), (25, "#6baed6"), (37.5, "#2171b5"), (50, "#08306b")]

def nodata_zero():
    return ('<noData><noDataList bandNo="1" useSrcNoData="0">'
            '<noDataRange min="0" max="0"/></noDataList></noData>')

def raster_layer(file_name, layer_name, renderer, drop_zero=False):
    e = raster_extent(os.path.join(PROJ, file_name))
    lid = re.sub(r"\W", "_", layer_name) + "_" + uuid.uuid4().hex
    xml = ('<maplayer type="raster" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" '
           'autoRefreshMode="Disabled" refreshOnNotifyEnabled="0">'
           f'<id>{lid}</id><datasource>../{file_name}</datasource>'
           f'<layername>{layer_name}</layername><provider>gdal</provider>'
           f'<srs>{CRS}</srs>{extent_xml(e)}'
           f'{nodata_zero() if drop_zero else ""}'
           f'<pipe>{renderer}'
           '<brightnesscontrast brightness="0" contrast="0" gamma="1"/>'
           '<huesaturation saturation="0" grayscaleMode="0" colorizeOn="0"/>'
           '<rasterresampler maxOversampling="2"/></pipe>'
           '<blendMode>0</blendMode></maplayer>')
    return lid, xml

def vector_layer(file_name, layer_name, symbol_xml, geom, layer_in_file=None):
    path = os.path.join(PROJ, file_name)
    e = vector_extent(path, layer_in_file)
    lid = re.sub(r"\W", "_", layer_name) + "_" + uuid.uuid4().hex
    source = f"../{file_name}" + (f"|layername={layer_in_file}" if layer_in_file else "")
    xml = ('<maplayer type="vector" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" '
           f'geometry="{geom}" autoRefreshMode="Disabled" refreshOnNotifyEnabled="0" '
           'simplifyDrawingHints="1" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" '
           'simplifyAlgorithm="0" readOnly="0" labelsEnabled="0" symbologyReferenceScale="-1">'
           f'<id>{lid}</id><datasource>{source}</datasource>'
           f'<layername>{layer_name}</layername><provider encoding="UTF-8">ogr</provider>'
           f'<srs>{CRS}</srs>{extent_xml(e)}'
           f'<renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0" '
           f'referencescale="-1"><symbols>{symbol_xml}</symbols></renderer-v2>'
           '<blendMode>0</blendMode><featureBlendMode>0</featureBlendMode></maplayer>')
    return lid, xml

def fill_symbol(stroke, width, fill_style="no", fill="0,0,0,0"):
    return ('<symbol type="fill" name="0" alpha="1" clip_to_extent="1" force_rhr="0" '
            'frame_rate="10" is_animated="0">'
            f'<layer class="SimpleFill" enabled="1" pass="0" locked="0" id="{{{uuid.uuid4()}}}">'
            '<Option type="Map">'
            f'<Option name="color" type="QString" value="{fill}"/>'
            f'<Option name="style" type="QString" value="{fill_style}"/>'
            f'<Option name="outline_color" type="QString" value="{stroke}"/>'
            f'<Option name="outline_width" type="QString" value="{width}"/>'
            '<Option name="outline_width_unit" type="QString" value="MM"/>'
            '<Option name="outline_style" type="QString" value="solid"/>'
            '<Option name="joinstyle" type="QString" value="bevel"/>'
            '</Option></layer></symbol>')

def marker_symbol(color, size):
    return ('<symbol type="marker" name="0" alpha="1" clip_to_extent="1" force_rhr="0" '
            'frame_rate="10" is_animated="0">'
            f'<layer class="SimpleMarker" enabled="1" pass="0" locked="0" id="{{{uuid.uuid4()}}}">'
            '<Option type="Map">'
            '<Option name="name" type="QString" value="circle"/>'
            f'<Option name="color" type="QString" value="{color}"/>'
            f'<Option name="size" type="QString" value="{size}"/>'
            '<Option name="size_unit" type="QString" value="MM"/>'
            '<Option name="outline_color" type="QString" value="35,35,35,255"/>'
            '<Option name="outline_width" type="QString" value="0.2"/>'
            '<Option name="outline_width_unit" type="QString" value="MM"/>'
            '<Option name="outline_style" type="QString" value="solid"/>'
            '<Option name="angle" type="QString" value="0"/>'
            '<Option name="offset" type="QString" value="0,0"/>'
            '<Option name="scale_method" type="QString" value="diameter"/>'
            '</Option></layer></symbol>')

# ---------------------------------------------------------------- layer set
def build_layers(stage):
    """Layers top-to-bottom, as the handout's step 1.9 lists them."""
    L = []
    if stage >= 3:
        L += [vector_layer("tour_stops.gpkg", "tour_stops",
                           fill_symbol("255,255,255,255", "0.8"), "Polygon", "tour_stops"),
              vector_layer("accommodation.gpkg", "accommodation",
                           marker_symbol("255,215,0,255", "2.2"), "Point", "accommodation"),
              vector_layer("osm_buildings_stops.gpkg", "osm_buildings_stops",
                           fill_symbol("120,120,120,255", "0.2", "solid", "200,200,200,140"),
                           "Polygon", "osm_buildings_stops"),
              vector_layer("protected_areas.shp", "protected_areas",
                           fill_symbol("30,160,60,255", "0.8"), "Polygon")]
    if stage >= 2:
        L += [raster_layer("viirs_vnl_v21_2021_average_masked_MWI.tif", "Lights 2021",
                           pseudocolor(0, 5, MAGMA), drop_zero=True),
              raster_layer("viirs_vnl_v21_2014_average_masked_MWI.tif", "Lights 2014",
                           pseudocolor(0, 5, MAGMA), drop_zero=True),
              raster_layer("ESA_WorldCover_10m_2021_v200_MWI.tif", "Built-up 2021",
                           paletted_builtup()),
              raster_layer("mwi_pop_2025_CN_100m_R2025A_v1.tif", "People 2025",
                           pseudocolor(0, 50, BLUES), drop_zero=True)]
    L += [raster_layer("Sentinel2_2025.tif", "Imagery 2025", rgb_renderer(), drop_zero=True),
          raster_layer("Sentinel2_2016.tif", "Imagery 2016", rgb_renderer(), drop_zero=True),
          raster_layer("malawi_s2_rgb_2021_30m.tif", "malawi_s2_rgb_2021_30m", rgb_renderer())]
    return L

def write_project(stage, out_name, title):
    layers = build_layers(stage)
    # the finished-Part-1 project opens in the state Part 2 asks for: stops and the two pictures
    on_at_start = {"tour_stops", "Imagery 2025", "Imagery 2016", "malawi_s2_rgb_2021_30m"}
    def checked(name):
        if stage < 3 or name in on_at_start:
            return "Qt::Checked"
        return "Qt::Unchecked"
    tree = "".join('<layer-tree-layer id="%s" name="%s" source="%s" providerKey="%s" '
                   'checked="%s" expanded="0"><customproperties/></layer-tree-layer>'
                   % (lid, re.search(r"<layername>(.*?)</layername>", xml).group(1),
                      re.search(r"<datasource>(.*?)</datasource>", xml).group(1),
                      "gdal" if 'type="raster"' in xml else "ogr",
                      checked(re.search(r"<layername>(.*?)</layername>", xml).group(1)))
                   for lid, xml in layers)
    order = "".join("<item>%s</item>" % lid for lid, _ in layers)
    canvas = raster_extent(os.path.join(PROJ, "malawi_s2_rgb_2021_30m.tif"))
    qgs = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<qgis projectname="%s" version="3.44.14-Solothurn">'
           '<homePath path=""/><title>%s</title>'
           '<projectCrs>%s</projectCrs>'
           '<layer-tree-group>%s<custom-order enabled="0">%s</custom-order></layer-tree-group>'
           '<mapcanvas name="theMapCanvas" annotationsVisible="1"><units>meters</units>%s'
           '<rotation>0</rotation><destinationsrs>%s</destinationsrs></mapcanvas>'
           '<projectlayers>%s</projectlayers>'
           '<layerorder>%s</layerorder>'
           '<properties><Measure><Ellipsoid type="QString">WGS84</Ellipsoid></Measure></properties>'
           '</qgis>'
           % (title, title, CRS, tree, order, extent_xml(canvas), CRS,
              "".join(xml for _, xml in layers),
              "".join('<layer id="%s"/>' % lid for lid, _ in layers)))
    os.makedirs(CKPT, exist_ok=True)
    out = os.path.join(CKPT, out_name)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(out_name.replace(".qgz", ".qgs"), qgs)
    print("wrote %s (%d layers)" % (out, len(layers)))

if __name__ == "__main__":
    write_project(1, "project1_checkpoint_1.qgz", "Project 1 - after step 1.4")
    write_project(2, "project1_checkpoint_2.qgz", "Project 1 - after step 1.7")
    write_project(3, "project1_start.qgz", "Project 1 - Part 1 finished")
