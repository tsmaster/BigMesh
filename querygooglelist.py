import urllib.request
import json
import requests

"""
Loads a list of locations (cities_by_pop.txt) and queries Google's
elevation service for their elevation.
reads: cities_by_pop.txt
"""

with open("api.key") as api_file:
    API_KEY = api_file.read().strip()


# with open("landmark_lat_lon.txt") as lmk_file:
with open("cities_by_pop.txt") as lmk_file:
    for lm_s in lmk_file.readlines():
        lm_s = lm_s.strip().split(",")

        lat = float(lm_s[0])
        lon = float(lm_s[1])

        q = "https://maps.googleapis.com/maps/api/elevation/json?locations={}%2C{}&key={}".format(
            lat, lon, API_KEY
        )

        r = requests.get(q)

        rj = r.json()
        print(rj)

        rj_res = rj["results"][0]

        rj_elev = rj_res["elevation"]

        rj_loc = rj_res["location"]

        rj_lat = rj_loc["lat"]
        rj_lon = rj_loc["lng"]

        print("lat:", rj_lat)
        print("lon:", rj_lon)
        print("elv:", rj_elev)
        print("\n\n")
