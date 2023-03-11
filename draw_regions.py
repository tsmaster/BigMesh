import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d

import point

"""
experiment to visualize points
reads: points.json
"""


point_list = point.read_pointlist_from_json("points.json")

lon_lats = [(p.lon, p.lat) for p in point_list]

# make up data points
point_array = np.array(lon_lats)

# compute Voronoi tesselation
vor = Voronoi(point_array)

print("points:", vor.points)
print("vertices:", vor.vertices)

# plot
fig = voronoi_plot_2d(vor, show_vertices=False, show_points=False)

import matplotlib.pyplot as plt


def get_point_index_from_region_index(ri):
    for p in range(len(vor.point_region)):
        if vor.point_region[p] == ri:
            return p
    return -1


# colorize
for ri, region in enumerate(vor.regions):
    pi = get_point_index_from_region_index(ri)
    if pi == -1:
        c = "red"
    else:
        pt = point_list[pi]
        if pt.elv > 0:
            c = "green"
        else:
            c = "blue"
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        plt.fill(*zip(*polygon), c)

plt.show()
