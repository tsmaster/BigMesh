import math
import random

import point
import googlefetch

"""
Generate points to populate Canada
reads: points.json
writes: points.json
"""


pointlist = point.read_pointlist_from_json("points.json")

count_in_last_day = point.count_created_in_recent_hours(24, pointlist)

print("count in last day", count_in_last_day)

count_to_add = 1300 - count_in_last_day

# see bridsonna for logic
# this gets canada and alaska

limit_north = 85
limit_south = 49
limit_west = -170
limit_east = -50

delta_east = abs(limit_west - limit_east)
delta_north = abs(limit_north - limit_south)
print("extent east-west:", delta_east)
print("extent north-south:", delta_north)

print("area in square degrees:", delta_east * delta_north)

point_spacing = 5.0

cell_width = point_spacing / math.sqrt(2.0)


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
    if (
        (p.lon < limit_west)
        or (p.lon > limit_east)
        or (p.lat < limit_south)
        or (p.lat > limit_north)
    ):
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
        if len(added_points) >= count_to_add:
            break

print("Found %d new points" % len(added_points))

for p in added_points:
    new_point = googlefetch.fetch(p.lat, p.lon)
    pointlist.append(new_point)

point.write_pointlist_to_json("points.json", pointlist)
