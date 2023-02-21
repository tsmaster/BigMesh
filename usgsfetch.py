import urllib.request
import json
import requests

import point


def fetch(lat, lon):
    q = "https://nationalmap.gov/epqs/pqs.php?y={}&x={}&output=json&units=Meters".format(
        lon, lat
    )

    r = requests.get(q)

    rj = r.json()

    rj_res = rj["USGS_Elevation_Point_Query_Service"]

    rj_elev = rj_res["Elevation_Query"]

    lat = rj_elev["y"]
    lon = rj_elev["x"]
    elv = rj_elev["Elevation"]

    print("got", lat, lon, elv)
    print(type(lat))
    print(type(lon))
    print(type(elv))

    try:
        elv = float(elv)
    except TypeError(e):
        print("got bogus elev")
        return None

    if elv == -1000000:
        print("got OOB elev")
        return None

    ret_pt = point.Point(lat, lon, elv, None)
    print("fetched", ret_pt)

    return ret_pt


if __name__ == "__main__":
    p = fetch(-120, 45)
    print(p)
