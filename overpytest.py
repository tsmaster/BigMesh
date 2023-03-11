import overpy

"""
Overpass test
"""

api = overpy.Overpass()

result = api.query(
    """
  way(47.79, -122.06, 47.8, -122.07) ["highway"];
  (._;>;);
  out body;
  """
)

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  hwy: %s" % way.tags.get("highway", "n/a"))
    print("  nodes:")
    for node in way.nodes:
        print("    lat: %f lon: %f" % (node.lat, node.lon))
