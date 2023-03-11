import math
import shapefile

import point

""" 
Pull in the boundary points of contents from continents shapefile

reads: points.json, NaturalEarth/ne_110m_land.zip
writes: points.json
"""

pointlist = point.read_pointlist_from_json("points.json")


# see bridsonna for logic
# this gets points along continent edges

point_spacing = 1.0

cell_width = point_spacing / math.sqrt(2.0)

limit_west = -180
limit_east = 180
limit_south = -90
limit_north = 90


def point_to_index(p):
    delta_east = p.lon - limit_west
    delta_north = p.lat - limit_south
    i_e = math.floor(delta_east / cell_width)
    i_n = math.floor(delta_north / cell_width)

    return (i_e, i_n)


background_grid = {}  # to be indexed by lat,lon integer pairs


def insert_point_in_grid(p):
    idx = point_to_index(p)

    old_list = background_grid.get(idx, [])

    old_list.append(p)

    background_grid[idx] = old_list


def can_insert_in_grid(p):
    if (p.lon < -180) or (p.lon > 180) or (p.lat < -89) or (p.lat > 89):
        return False

    idx = point_to_index(p)

    ix, iy = idx

    for probe_x in range(ix - 2, ix + 3):
        for probe_y in range(iy - 2, iy + 3):
            probe_idx = (probe_x, probe_y)
            if probe_idx in background_grid:
                for stored_point in background_grid[probe_idx]:
                    d = stored_point.dist(p)
                    if d < point_spacing:
                        return False
    return True


k = 30

open_set = []

added_points = []

for p in pointlist:
    if (
        (p.lon >= limit_west - 2)
        and (p.lon <= limit_east + 2)
        and (p.lat >= limit_south - 2)
        and (p.lat <= limit_north + 2)
    ):
        # print ("found point:", p)
        open_set.append(p)
        insert_point_in_grid(p)


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

    for sp in shp.points:
        print("shape point", sp)
        lon = sp[0]
        lat = sp[1]
        elv = -0.0001234
        p = point.Point(lat, lon, elv, None)

        if can_insert_in_grid(p):
            print("inserting coast point", p)
            insert_point_in_grid(p)
            added_points.append(p)


print("Found %d new points" % len(added_points))

for p in added_points:
    # new_point = usgsfetch.fetch(p.lat, p.lon)
    # new_point = googlefetch.fetch(p.lat, p.lon)
    # if new_point:
    #    pointlist.append(new_point)
    pointlist.append(p)

point.write_pointlist_to_json("points.json", pointlist)
