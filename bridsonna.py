import math
import random

import point
import googlefetch

"""
Generates points for North America
reads: points.json
writes: points.json
"""

pointlist = point.read_pointlist_from_json("points.json")

count_in_last_day = point.count_created_in_recent_hours(24, pointlist)

print("count in last day", count_in_last_day)

count_to_add = 1300 - count_in_last_day


"""
From the PDF
https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf


The algorithm takes as input the extent of the sample domain in
R^n, the minimum distance r between samples, and a constant k
as the limit of samples to choose before rejection in the algorithm
(typically k = 30).

Step 0. Initialize an n-dimensional background grid for storing
samples and accelerating spatial searches. We pick the cell size to
be bounded by r/sqrt(n), so that each grid cell will contain at most
one sample, and thus the grid can be implemented as a simple 
n-dimensional array of integers: the default −1 indicates no sample, a
non-negative integer gives the index of the sample located in a cell.

Step 1. Select the initial sample, x0, randomly chosen uniformly
from the domain. Insert it into the background grid, and initialize
the “active list” (an array of sample indices) with this index (zero).

Step 2. While the active list is not empty, choose a random index
from it (say i). Generate up to k points chosen uniformly from the
spherical annulus between radius r and 2r around xi. For each
point in turn, check if it is within distance r of existing samples
(using the background grid to only test nearby samples). If a point
is adequately far from existing samples, emit it as the next sample
and add it to the active list. If after k attempts no such point is
found, instead remove i from the active list.
"""

"""
And then the improvement, from
http://extremelearning.com.au/an-improved-version-of-bridsons-algorithm-n-for-poisson-disc-sampling/#:~:text=Bridson's%20Algorithm%20(2007)%20is%20a,than%20a%20specified%20distance%20apart.

Also https://observablehq.com/@techsparx/an-improvement-on-bridsons-algorithm-for-poisson-disc-samp/2

Insight here is to sample along the inner boundary of the acceptable annulus.
"""

limit_north = 49
limit_south = 25
limit_west = -125
limit_east = -65

delta_east = abs(limit_west - limit_east)
delta_north = abs(limit_north - limit_south)
print("extent east-west:", delta_east)
print("extent north-south:", delta_north)

print("area in square degrees:", delta_east * delta_north)

point_spacing = 1.0

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
