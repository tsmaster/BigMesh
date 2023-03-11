import math

"""
Math convenience functions
"""


# ----------------------------------------
# generic convenience operators
# ----------------------------------------


def bdg_map(v, in_min, in_max, out_min, out_max):
    t = (v - in_min) / (in_max - in_min)
    return out_min + t * (out_max - out_min)


def clamp(v, min_val, max_val):
    v = max(v, min_val)
    v = min(v, max_val)
    return v


# ----------------------------------------
# angles
# ----------------------------------------


def deg_to_rad(d):
    return bdg_map(d, 0.0, 360.0, 0.0, 2 * math.pi)


def rad_to_deg(r):
    return bdg_map(r, 0.0, 2 * math.pi, 0.0, 360.0)


# ----------------------------------------
# Web Mercator
# ----------------------------------------
# see https://en.wikipedia.org/wiki/Web_Mercator_projection


def lat_lon_to_wm_xy(lat, lon):
    lon_rad = deg_to_rad(lon)
    lat_rad = deg_to_rad(lat)

    x = (256 / (2 * math.pi)) * (lon_rad + math.pi)
    y = (256 / (2 * math.pi)) * (
        math.pi - math.log(math.tan(math.pi / 4.0 + lat_rad / 2.0))
    )

    return (x, y)


# ----------------------------------------
# Haversine
# ----------------------------------------


def haversine_distance_deg(lat_1, lon_1, lat_2, lon_2):
    # from https://www.movable-type.co.uk/scripts/latlong.html

    lat_1_r = deg_to_rad(lat_1)
    lon_1_r = deg_to_rad(lon_1)
    lat_2_r = deg_to_rad(lat_2)
    lon_2_r = deg_to_rad(lon_2)

    delta_lat = lat_2_r - lat_1_r
    delta_lon = lon_2_r - lon_1_r

    sin_lat_over_two = math.sin(delta_lat / 2.0)
    cos_lat_1 = math.cos(lat_1_r)
    cos_lat_2 = math.cos(lat_2_r)
    sin_lon_over_two = math.sin(delta_lon / 2.0)

    a = (
        sin_lat_over_two * sin_lat_over_two
        + cos_lat_1 * cos_lat_2 * sin_lon_over_two * sin_lon_over_two
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    # c is angle in radians, return distance in DEGREES
    return rad_to_deg(c)


def haversine_offset_deg(lat, lon, heading, distance_deg):
    # from https://www.movable-type.co.uk/scripts/latlong.html
    # "Destination point given distance and bearing from start point"

    lat_1_r = deg_to_rad(lat)
    lon_1_r = deg_to_rad(lon)

    azimuth_r = deg_to_rad(heading)  # clockwise from north

    distance_r = deg_to_rad(distance_deg)

    lat_2_r = math.asin(
        math.sin(lat_1_r) * math.cos(distance_r)
        + math.cos(lat_1_r) * math.sin(distance_r) * math.cos(azimuth_r)
    )
    lon_2_r = lon_1_r + math.atan2(
        math.sin(azimuth_r) * math.sin(distance_r) * math.cos(lat_1_r),
        math.cos(distance_r) - math.sin(lat_1_r) * math.sin(lat_2_r),
    )

    return rad_to_deg(lat_2_r), rad_to_deg(lon_2_r)
