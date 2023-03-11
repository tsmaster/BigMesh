# benchmarking getting roads from NH using PyrOSM

import os

"""
experiment to test downloading OSM data
"""

os.environ["USE_PYGEOS"] = "0"
import geopandas


from pyrosm import OSM, get_data
import time

# Initialize (downloads data automatically for New Hampshire)
fp = get_data("new_hampshire", directory="OSM")
osm = OSM(fp)

# Parse roads and time it
start_time = time.time()
roads = osm.get_network("driving")
print(f"Parsing roads lasted {round(time.time() - start_time, 0)} seconds.")
print(f"Number of roads parsed: {len(roads)}")
