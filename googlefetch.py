import urllib.request
import json
import requests

import point

"""
imports elevations for lat/lon from google elevation service
"""

with open("api.key") as api_file:
    API_KEY = api_file.read().strip()


def fetch(lat, lon):
    q = "https://maps.googleapis.com/maps/api/elevation/json?locations={}%2C{}&key={}".format(
        lat, lon, API_KEY
    )

    r = requests.get(q)

    rj = r.json()

    rj_res = rj["results"][0]

    rj_elev = rj_res["elevation"]

    rj_loc = rj_res["location"]

    rj_lat = rj_loc["lat"]
    rj_lon = rj_loc["lng"]

    ret_pt = point.Point(lat, lon, rj_elev, None)
    print("fetched", ret_pt)

    return ret_pt
