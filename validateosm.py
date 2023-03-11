import os

os.environ["USE_PYGEOS"] = "0"
import geopandas


import glob
import pyrosm

"""
opens OSM files, hoping to identify files that don't open
reads: OSM/*.osm.pbf
"""

filenames = glob.glob("OSM/*.osm.pbf")
filenames.sort()

for fn in filenames:
    print("validating fn", fn)

    try:
        osm = pyrosm.OSM(fn)
        drive_net = osm.get_network(network_type="driving")
        drive_net.plot()
    except TypeError as te:
        print("got type error")
    except ValueError as ve:
        print("value error", ve)
    except pyrosm.DecodeError as de:
        print("decode error", de)
