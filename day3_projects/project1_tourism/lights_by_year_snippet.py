# ===========================================================================
# TOOL: night lights for every year, summed inside each tour stop.
#
# You are not expected to be able to write this, and you will not be asked to.
# It does Extension A once per year instead of once, because clicking through
# eleven years by hand is slow and easy to get wrong.
#
# HOW TO USE IT
#   1. In QGIS: Plugins > Python Console. Click the "Show Editor" button.
#   2. Open this file in the editor, change the two lines marked CHANGE ME,
#      and press the green Run button.
#   3. It prints a table and saves a CSV you can open in Excel.
#
# Your project must already have the tour_stops layer loaded (Part 1).
# ===========================================================================

# CHANGE ME 1 - the folder with the yearly night lights files.
lights_folder = "/Users/you/Desktop/project1_tourism/nightlights_all_years"

# CHANGE ME 2 - where to save the table.
output_csv = "/Users/you/Desktop/project1_tourism/outputs/lights_by_year.csv"

# --------------------------------------------------------------------------
# Nothing below here needs changing.
# --------------------------------------------------------------------------
import csv
import glob
import os

import processing
from qgis.core import QgsProject

stops = QgsProject.instance().mapLayersByName("tour_stops")[0]

files = sorted(glob.glob(os.path.join(lights_folder, "*.tif")))
if not files:
    raise SystemExit("No .tif files found in %s - check CHANGE ME 1." % lights_folder)

totals = {}   # {stop name: {year: sum of light}}
years = []
for path in files:
    year = os.path.basename(path).split("_")[3][:4]
    years.append(year)
    result = processing.run("native:zonalstatisticsfb", {
        "INPUT": stops,
        "INPUT_RASTER": path,
        "RASTER_BAND": 1,
        "COLUMN_PREFIX": "light_",
        "STATISTICS": [1],            # 1 = sum
        "OUTPUT": "TEMPORARY_OUTPUT",
    })["OUTPUT"]
    for feature in result.getFeatures():
        value = feature["light_sum"]
        totals.setdefault(feature["name"], {})[year] = 0.0 if value is None else float(value)
    print("done %s" % year)

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, "w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["stop"] + years)
    for name in sorted(totals):
        writer.writerow([name] + ["%.1f" % totals[name][y] for y in years])

print("")
print("%-30s %s" % ("stop", "  ".join(years)))
for name in sorted(totals):
    print("%-30s %s" % (name, "  ".join("%5.1f" % totals[name][y] for y in years)))
print("")
print("Saved: %s" % output_csv)
