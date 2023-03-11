import math
import shapefile

from PIL import Image, ImageDraw

from bdgmath import lat_lon_to_wm_xy
import bdgmath

"""
experiment to draw state boundaries
reads: 
  NaturalEarth/ne_110m_land.zip
  NaturalEarth/ne_110m_admin_1_states_provinces.zip
  NaturalEarth/110m_physical.zip/ne_110m_lakes.shp
  Tiles/voronoi.json
writes: 
  states.png
"""

west_limit = -125
east_limit = -65
north_limit = 50
south_limit = 25

west_x, south_y = lat_lon_to_wm_xy(south_limit, west_limit)
east_x, north_y = lat_lon_to_wm_xy(north_limit, east_limit)

IM_WIDTH = 2000
IM_HEIGHT = int((south_y - north_y) * IM_WIDTH / (east_x - west_x))

print("im width, height", IM_WIDTH, IM_HEIGHT)


def draw_shapefile(fn, draw, fill, outline):
    sf = shapefile.Reader(fn)
    shapes = sf.shapes()

    for shape in shapes:
        for part_index_index, part_index in enumerate(shape.parts):
            if part_index_index + 1 == len(shape.parts):
                last_index = len(shape.points)
            else:
                last_index = shape.parts[part_index_index + 1]

            poly_points = []

            for i in range(part_index, last_index):
                spi = shape.points[i]

                s_lat = bdgmath.clamp(spi[1], -85.0, 85.0)
                s_lon = bdgmath.clamp(spi[0], -180.0, 180.0)

                try:
                    ix, iy = lat_lon_to_wm_xy(s_lat, s_lon)
                except ValueError as ve:
                    print(ve)
                    print(i, spi)

                ix = bdgmath.bdg_map(ix, west_x, east_x, 0, IM_WIDTH)
                iy = bdgmath.bdg_map(iy, north_y, south_y, 0, IM_HEIGHT)

                poly_points.append((ix, iy))
            draw.polygon(poly_points, fill=fill, outline=outline)


im = Image.new("RGBA", (IM_WIDTH, IM_HEIGHT), (100, 100, 255, 255))
draw = ImageDraw.Draw(im)

land_fn = "NaturalEarth/ne_110m_land.zip"
state_fn = "NaturalEarth/ne_110m_admin_1_states_provinces.zip"
lake_fn = "NaturalEarth/110m_physical.zip/ne_110m_lakes.shp"

draw_shapefile(land_fn, draw, (80, 160, 80), (50, 100, 50))  # fill  # outline

draw_shapefile(state_fn, draw, (100, 200, 100), (50, 100, 50))  # fill  # outline

draw_shapefile(lake_fn, draw, (0, 0, 200), (100, 100, 200))  # fill  # outline


# also draw points?
"""
import point
points = point.read_pointlist_from_json('points.json')

for p in points:
    x,y = lat_lon_to_wm_xy(p.lat, p.lon)
    x *= scale
    y *= scale
    
    clr = (200, 100, 0)
    if p.elv < 0:
        clr = (100, 100, 200)

    r = 5
    draw.ellipse((x-r, y-r, x+r, y+r), fill=clr)
"""

# also draw tiles

import json

with open("Tiles/voronoi.json") as vj:
    vdict = json.loads(vj.read())

    for p in vdict["points"]:
        p_lat = p["lat"]
        p_lon = p["lon"]

        x, y = lat_lon_to_wm_xy(p_lat, p_lon)

        x = bdgmath.bdg_map(x, west_x, east_x, 0, IM_WIDTH)
        y = bdgmath.bdg_map(y, north_y, south_y, 0, IM_HEIGHT)

        clr = (100, 100, 200)
        r = 1.5
        draw.ellipse((x - r, y - r, x + r, y + r), fill=clr)

    for r in vdict["regions"]:
        region_points = []

        if -1 in r["vert_indices"]:
            continue
        if len(r["vert_indices"]) == 0:
            continue

        for vi in r["vert_indices"]:
            p = vdict["vertices"][vi]

            p_lat = p["lat"]
            p_lon = p["lon"]

            """
            if ((p_lat > 85) or
                (p_lat < -85) or
                (p_lon > 180) or
                (p_lon < -180)):
                break
            """
            p_lat = bdgmath.clamp(p_lat, -85.0, 85.0)
            p_lon = bdgmath.clamp(p_lon, -180, 180)

            try:
                x, y = lat_lon_to_wm_xy(p_lat, p_lon)
            except ValueError as ve:
                print(ve)
                print(p_lat, p_lon)
                print(vi, p)
                print(r)

            x = bdgmath.bdg_map(x, west_x, east_x, 0, IM_WIDTH)
            y = bdgmath.bdg_map(y, north_y, south_y, 0, IM_HEIGHT)

            region_points.append((x, y))

        if len(region_points) < 3:
            continue

        # region_points.append(region_points[0])
        clr = (150, 150, 150)
        # draw.line(region_points, fill=clr, width = 3)
        draw.polygon(region_points, fill=None, outline=clr)


im.save("states.png")
