import shapefile

"""
test for reading continent data
reads:
  NaturalEarth/ne_110m_land.zip
"""

sf = shapefile.Reader("NaturalEarth/ne_110m_land.zip")

print("shapetype:", sf.shapeType)
print("shape type name:", sf.shapeTypeName)

shapetype_dict = {0: "null", 1: "point", 3: "polyline", 5: "polygon"}

if sf.shapeType in shapetype_dict:
    print("shape type:", shapetype_dict[sf.shapeType])

print("num features:", len(sf))
print("bbox", sf.bbox)

shapes = sf.shapes()

for shape_index in range(len(shapes)):
    shp = sf.shape(shape_index)
    print()
    print("shape", shape_index)
    print("  bbox", shp.bbox)
    print("  oid", shp.oid)
    print("  parts", shp.parts)
    # print("  points", shp.points)
    print("  shapeType", shp.shapeType)
    print("  shapeTypeName", shp.shapeTypeName)
