import math
import random

import point

# import usgsfetch
import googlefetch

pointlist = point.read_pointlist_from_json("points.json")

# see bridsonna for logic
# this gets points outside US and Canada

point_spacing = 12.0

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


while open_set:
    p_idx = random.randrange(len(open_set))
    p = open_set[p_idx]

    # Martin Roberts' method:
    # take k attempts to find a valid point
    # spaced at our minimal acceptable distance
    # in a random direction

    seed = random.random()
    epsilon = 0.000001

    inserted = False

    for j in range(k):
        theta = 2 * math.pi * (seed + float(j) / k)
        r = point_spacing + epsilon
        new_east = p.lon + r * math.cos(theta)
        new_north = p.lat + r * math.sin(theta)

        candidate_point = point.Point(new_north, new_east, None, None)

        if can_insert_in_grid(candidate_point):
            print("inserting", candidate_point)
            insert_point_in_grid(candidate_point)
            inserted = True
            break

    if not inserted:
        del open_set[p_idx]

    else:
        added_points.append(candidate_point)
        open_set.append(candidate_point)

print("Found %d new points" % len(added_points))

for p in added_points:
    # new_point = usgsfetch.fetch(p.lat, p.lon)
    new_point = googlefetch.fetch(p.lat, p.lon)
    if new_point:
        pointlist.append(new_point)

point.write_pointlist_to_json("points.json", pointlist)
