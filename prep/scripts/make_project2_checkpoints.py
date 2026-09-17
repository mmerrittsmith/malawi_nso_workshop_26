#!/usr/bin/env python3
"""Build the three checkpoints for mini-project 2 (urban growth in Zomba).

Writes day3_projects/project2_zomba_urban_growth/checkpoints/:
  project2_checkpoint_1.qgz  after Part 1 - the 2016 and 2026 pictures, ready to flip between
  project2_checkpoint_2.qgz  after Part 2 - plus built-up surface 2015 and 2020, styled
  project2_checkpoint_3.qgz  after Part 4 - plus new built-up, growth areas, buildings, boundaries

Paths are relative, so a checkpoint works from a copy of the project folder.
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qgs_build as q

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROJ = os.path.join(ROOT, "day3_projects", "project2_zomba_urban_growth")
CKPT = os.path.join(PROJ, "checkpoints")
q.BASE["dir"] = PROJ

# built-up surface is m2 per 100 m cell (0-10000); 0 transparent so the picture shows through.
# Magma, matching the night lights in project 1, and a ramp QGIS ships with by default.
BUILT = [(0, "#000004"), (1250, "#51127c"), (2500, "#b73779"), (3750, "#fc8961"), (5000, "#fcfdbf")]

def pseudocolor(vmin, vmax, stops):
    items = "".join('<item value="%s" color="%s" alpha="%d" label="%g"/>'
                    % (v, c, 0 if i == 0 else 255, v) for i, (v, c) in enumerate(stops))
    return ('<rasterrenderer type="singlebandpseudocolor" band="1" opacity="1" alphaBand="-1" '
            f'classificationMin="{vmin}" classificationMax="{vmax}" nodataColor="">'
            '<rastershader><colorrampshader colorRampType="INTERPOLATED" classificationMode="1" '
            f'clip="0" minimumValue="{vmin}" maximumValue="{vmax}" labelPrecision="0">{items}'
            '</colorrampshader></rastershader></rasterrenderer>')

def layers(stage):
    """Top to bottom, as the Layers panel should read at the end of each part."""
    L = []
    if stage >= 3:
        L += [q.vector_layer("./data/growth_areas.gpkg", "growth_areas",
                             q.fill("227,26,28,255", "0.6", "solid", "227,26,28,90"),
                             "Polygon", "growth_areas", 32736, "MultiPolygon"),
              q.vector_layer("../zomba_areas.gpkg", "zomba_areas",
                             q.fill("255,255,255,255", "0.8"), "Polygon", "zomba_areas",
                             32736, "MultiPolygon"),
              q.vector_layer("../zomba_buildings.shp", "zomba_buildings",
                             q.fill("110,110,110,255", "0.2", "solid", "220,220,220,130"),
                             "Polygon"),
              q.raster_layer("./data/new_builtup.tif", "new built-up 2015-2020",
                             q.mask("#e31a1c", "gained > 500 m2"))]
    if stage >= 2:
        L += [q.raster_layer("../Zomba_builtup_2020_GHSL.tif", "Built-up 2020",
                             pseudocolor(0, 5000, BUILT)),
              q.raster_layer("../Zomba_builtup_2015_GHSL.tif", "Built-up 2015",
                             pseudocolor(0, 5000, BUILT))]
    L += [q.raster_layer("../Zomba_Sentinel2_RGB_20260720.tif", "Imagery 2026", q.rgb(1, 3000)),
          q.raster_layer("../Zomba_Sentinel2_RGB_20160730.tif", "Imagery 2016", q.rgb(1, 3000))]
    return L

def write(stage, name, title):
    L = layers(stage)
    import re
    tree = "".join('<layer-tree-layer id="%s" name="%s" source="%s" providerKey="%s" '
                   'checked="Qt::Checked" expanded="0"><customproperties/></layer-tree-layer>'
                   % (lid, nm, re.search(r"<datasource>(.*?)</datasource>", xml).group(1),
                      "gdal" if 'type="raster"' in xml else "ogr")
                   for lid, xml, nm in L)
    canvas = q.raster_extent("../Zomba_Sentinel2_RGB_20160730.tif")
    qgs = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<qgis projectname="{title}" version="3.44.14-Solothurn">'
           f'<homePath path=""/><title>{title}</title><projectCrs>{q.CRS}</projectCrs>'
           f'<layer-tree-group>{tree}<custom-order enabled="0">'
           + "".join("<item>%s</item>" % lid for lid, _, _ in L)
           + '</custom-order></layer-tree-group>'
           '<mapcanvas name="theMapCanvas" annotationsVisible="1"><units>meters</units>'
           f'{q.extent_xml(canvas)}<rotation>0</rotation><destinationsrs>{q.CRS}</destinationsrs>'
           '</mapcanvas>'
           '<projectlayers>' + "".join(xml for _, xml, _ in L) + '</projectlayers>'
           '<layerorder>' + "".join('<layer id="%s"/>' % lid for lid, _, _ in L) + '</layerorder>'
           '<properties><Measure><Ellipsoid type="QString">WGS84</Ellipsoid></Measure></properties>'
           '</qgis>')
    os.makedirs(CKPT, exist_ok=True)
    with zipfile.ZipFile(os.path.join(CKPT, name), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(name.replace(".qgz", ".qgs"), qgs)
    print("wrote %s (%d layers)" % (name, len(L)))

if __name__ == "__main__":
    write(1, "project2_checkpoint_1.qgz", "Project 2 - after Part 1")
    write(2, "project2_checkpoint_2.qgz", "Project 2 - after Part 2")
    write(3, "project2_checkpoint_3.qgz", "Project 2 - after Part 4")
