import math
import os
import random
import re
import subprocess

from PIL import Image, ImageDraw

import bdgmath

"""
collects city data from state protocol buffer files, 
sorts city by population,
creates a bridson blue noise map starting with cities, populating with point spacing 1.0
generates tile polygons using voronoi

reads: OSM/*-latest.osm.pbf
writes: 
  map.png
  Tiles/voronoi.json
  Tiles/tile_*.json
"""

# from pyrosm import get_data

# rainbow
# west_limit = -123
# east_limit = -122
# north_limit = 48
# south_limit = 47

# washington
# west_limit = -125
# east_limit = -116
# north_limit = 49
# south_limit = 46

# sea->bos
west_limit = -125
east_limit = -65
north_limit = 49
south_limit = 40

# continental US
west_limit = -125
east_limit = -65
north_limit = 49
south_limit = 25

stateToAbbrevDict = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}


class State:
    def __init__(self, name, osm_filename=None):
        self.name = name.title().replace("-", " ")
        self.abbrev = stateToAbbrevDict[self.name]
        self.osm_filename = osm_filename
        if osm_filename is None:
            self.osm_filename = self.name.lower().replace(" ", "-")

    def __lt__(self, o):
        return self.name < o.name


def make_rainbow():
    states = ["rainbow.pbf"]
    return states


def make_sea_to_bos():
    # sea->bos states

    states = [
        "washington",
        "idaho",
        # "montana",
        # "north-dakota",
        # "minnesota",
        # "wisconsin",
        # "illinois",
        # "indiana",
        # "ohio",
        # "pennsylvania",
        # "new-york",
        # "massachusetts"
    ]

    return [State(s) for s in states]


def make_continental_us():
    # all continental US states

    states = [
        "Alabama",
        # "Alaska",
        "Arizona",
        "Arkansas",
        # "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        # "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]

    states = [State(s) for s in states] + [
        State("California", "norcal"),
        State("California", "socal"),
    ]

    states.sort()

    return states


if True:
    states = make_continental_us()
else:
    states = make_sea_to_bos()

rel_path = "OSM"
suffix = "-latest.osm.pbf"
# suffix = ""

IM_WIDTH = 6000
IM_HEIGHT = 3500


def bdg_map(v, in_min, in_max, out_min, out_max):
    f = (v - in_min) / (in_max - in_min)
    return out_min + f * (out_max - out_min)


im = Image.new("RGB", (IM_WIDTH, IM_HEIGHT), (128, 200, 128))
draw = ImageDraw.Draw(im)


class City:
    def __init__(self, name, state_name, lat, lon, pop):
        self.name = name
        self.state_name = state_name
        self.lat = lat
        self.lon = lon
        self.pop = pop

    def __lt__(self, o):
        return self.pop < o.pop

    def __str__(self):
        return "%s, %s (%f, %f) p: %d" % (
            self.name,
            self.state_name,
            self.lat,
            self.lon,
            self.pop,
        )

    def __repr__(self):
        return str(self)

    def dist(self, other):
        return bdgmath.haversine_distance_deg(self.lat, self.lon, other.lat, other.lon)


cities = []

for s in states:
    im.save("map.png")

    print("state: %s (%s)" % (s.name, s.abbrev))

    # fp = get_data(s, directory=rel_path)

    p = os.path.join(rel_path, s.osm_filename + suffix)

    print(p)

    cmd = "./DrawMap/drawmap/target/release/drawmap " + p
    print(cmd)

    proc = subprocess.run(cmd.split(), capture_output=True)

    print("returncode:", proc.returncode)

    out_lines = str(proc.stdout, "UTF-8").split("\n")
    # for o in out_lines:
    #    print(o)

    color = (255, 0, 0)

    if proc.returncode == 0:
        state_cities = []

        for line in out_lines:
            # print(line)
            if line.startswith("Found a city:"):
                # print(line)
                m = re.search(
                    'name="([A-Za-z ]+)" lat=([0-9\.-]*), lon=([0-9\.-]*), population=([0-9]+)',
                    line,
                )
                # print ("city match?", m)
                if m:
                    # print(m[1])
                    # print(m[2])
                    # print(m[3])
                    # print(m[4])

                    name = m[1]
                    lat = float(m[2])
                    lon = float(m[3])
                    pop = int(m[4])

                    city = City(name, s.name, lat, lon, pop)
                    state_cities.append(city)
                    print("city:", city)

            if line == "highway":
                color = (64, 64, 64)
                # print("got hwy")
            if line == "Found a boundary":
                color = (0, 0, 128)
                # print("got boundary")
            if line.startswith("pl:"):
                coords = []

                if color == (0, 0, 128):
                    continue

                if "[" in line and "]" in line:
                    left = line.index("[")
                    right = line.index("]")
                    line = line[left + 1 : right]
                    # print ("stripped line:", line)

                    while line:
                        if "(" in line and ")" in line:
                            left = line.index("(")
                            right = line.index(")")
                            coord_str = line[left + 1 : right]
                            # print ("found coord", coord_str)
                            line = line[right + 1 :]

                            terms = coord_str.split(",")
                            coords.append((float(terms[0]), float(terms[1])))
                        else:
                            break

                # print("parsed coords:", coords)

                im_coords = []
                for c in coords:
                    c_lat, c_lon = c
                    ix = bdg_map(c_lon, west_limit, east_limit, 0, IM_WIDTH)
                    iy = bdg_map(c_lat, north_limit, south_limit, 0, IM_HEIGHT)
                    im_coords.append((ix, iy))

                # print("drawing", im_coords)

                draw.line(im_coords, fill=color, width=2)
                # exit(-1)

        for sc in state_cities:
            ix = bdg_map(sc.lon, west_limit, east_limit, 0, IM_WIDTH)
            iy = bdg_map(sc.lat, north_limit, south_limit, 0, IM_HEIGHT)

            radius = 3.5

            draw.ellipse(
                (ix - radius, iy - radius, ix + radius, iy + radius),
                fill=(255, 192, 0),
            )
            cities.append(sc)

    else:
        print("error")
        err_lines = str(proc.stderr, "UTF-8").split("\n")
        for e in err_lines:
            print("ERR:  ", e)

cities.sort()
cities = cities[::-1]

print()
print()

for ci, c in enumerate(cities):
    print(ci, c)

im.save("map.png")


# ----------------------------------------
# Bridsonize
# ----------------------------------------

grid = {}

point_spacing = 1.0

cell_size = point_spacing / math.sqrt(2.0)


def lat_lon_to_index(lat, lon):
    ix = math.floor((lon - west_limit) / cell_size)
    iy = math.floor((lat - south_limit) / cell_size)

    return (ix, iy)


def can_insert(lat, lon):
    if (
        (lon < west_limit)
        or (lon > east_limit)
        or (lat < south_limit)
        or (lat > north_limit)
    ):
        return False

    ix, iy = lat_lon_to_index(lat, lon)

    for dx in range(-2, 3):
        px = ix + dx
        for dy in range(-2, 3):
            py = iy + dy

            probe_key = (px, py)
            if probe_key in grid:
                g_lat, g_lon = grid[probe_key]

                d_lat = lat - g_lat
                d_lon = lon - g_lon

                # dist = math.sqrt(d_lat * d_lat + d_lon * d_lon)
                dist = bdgmath.haversine_distance_deg(lat, lon, g_lat, g_lon)

                if dist <= point_spacing:
                    return False
    return True


open_points = []
added_points = []

for c in cities:
    if can_insert(c.lat, c.lon):
        ci = lat_lon_to_index(c.lat, c.lon)
        grid[ci] = (c.lat, c.lon)
        print("inserted", c)
        open_points.append((c.lat, c.lon))
        added_points.append((c.lat, c.lon))

k = 30

while open_points:
    p_lat, p_lon = open_points[0]
    open_points = open_points[1:]

    p = (p_lat, p_lon)

    # print("examining", p)

    seed = random.random()
    epsilon = 0.000001

    inserted = False

    for j in range(k):
        # theta = 2 * math.pi * (seed + float(j) / k)
        heading = 360.0 * (seed + float(j) / k)

        r = point_spacing + epsilon
        # new_lat = p_lat + r * math.sin(theta)
        # new_lon = p_lon + r * math.cos(theta)
        new_lat, new_lon = bdgmath.haversine_offset_deg(p_lat, p_lon, heading, r)

        if can_insert(new_lat, new_lon):
            ni = lat_lon_to_index(new_lat, new_lon)
            grid[ni] = (new_lat, new_lon)
            open_points.append((new_lat, new_lon))
            inserted = True
            # print("inserted new point", new_lat, new_lon)
            added_points.append((new_lat, new_lon))

            # --- draw ---

            ix = bdg_map(new_lon, west_limit, east_limit, 0, IM_WIDTH)
            iy = bdg_map(new_lat, north_limit, south_limit, 0, IM_HEIGHT)

            radius = 3.5

            draw.ellipse(
                (ix - radius, iy - radius, ix + radius, iy + radius),
                fill=(0, 0, 64),
            )


im.save("map.png")

# ----------------------------------------
# voronoi
# ----------------------------------------
# see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html

import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d

xys = [(p[1], p[0]) for p in added_points]
# make up data points
point_array = np.array(xys)

# compute Voronoi tesselation
vor = Voronoi(point_array)

print("points:", vor.points)
print("vertices:", vor.vertices)

# write json
import json
import glob
import os

for fn in glob.glob("Tiles/*.json"):
    os.unlink(fn)

with open("Tiles/voronoi.json", "wt") as vf:
    data = {}

    point_list = []
    for pi, p in enumerate(vor.points):
        point_list.append({"lat": p[1], "lon": p[0], "point_index": pi})
    data["points"] = point_list

    vert_list = []
    for pi, p in enumerate(vor.vertices):
        vert_list.append({"lat": p[1], "lon": p[0], "vert_index": pi})
    data["vertices"] = vert_list

    region_list = []
    for ri, r in enumerate(vor.regions):
        if -1 in r:
            continue

        if len(r) == 0:
            continue

        r_data = {"vert_indices": r, "region_index": ri}
        region_list.append(r_data)
    data["regions"] = region_list

    vf.write(json.dumps(data, indent=2))

# make tile objects
import tile
import point

print("going to try to save %d regions" % len(vor.regions))
print("I have %d points" % len(vor.points))

region_to_point_map = {}
for pi in range(len(vor.points)):
    ri = vor.point_region[pi]
    region_to_point_map[ri] = pi


tiles = []

for ri, r in enumerate(vor.regions):
    if -1 in r:
        continue
    if len(r) == 0:
        continue

    if ri not in region_to_point_map:
        print("error, running off end of points")
        break

    t = tile.Tile()
    pi = region_to_point_map[ri]
    p = vor.points[pi]
    tile_centroid = point.Point(p[1], p[0], None, None)
    t.centroid_lat_lon = tile_centroid
    t.tile_id = pi

    verts = []
    for vi in r:
        p = vor.vertices[vi]
        pt = point.Point(p[1], p[0], None, None)
        verts.append(pt)
    t.verts_lat_lon = verts
    t.make_bbox_lat_lon()

    # todo more population

    tiles.append(t)

for c in cities:
    for t in tiles:
        if t.point_in_tile_lat_lon(c.lat, c.lon):
            t.city_list.append(c.name)
            if c.state_name not in t.state_list:
                t.state_list.append(c.state_name)
                t.state_list.sort()

for t in tiles:
    fn = "Tiles/tile_%04d.json" % (t.tile_id)
    t.to_json(fn)

for region in vor.regions:
    if -1 in region:
        continue

    polygon = [vor.vertices[i] for i in region]

    for i in range(len(polygon)):
        j = i - 1

        x1, y1 = polygon[i]
        x2, y2 = polygon[j]

        i_x1 = bdg_map(x1, west_limit, east_limit, 0, IM_WIDTH)
        i_y1 = bdg_map(y1, north_limit, south_limit, 0, IM_HEIGHT)
        i_x2 = bdg_map(x2, west_limit, east_limit, 0, IM_WIDTH)
        i_y2 = bdg_map(y2, north_limit, south_limit, 0, IM_HEIGHT)

        try:
            draw.line((i_x1, i_y1, i_x2, i_y2), fill=(255, 20, 20), width=3)
        except ValueError as ve:
            print("value error drawing line", i_x1, i_y1, i_x2, i_y2)


im.save("map.png")
