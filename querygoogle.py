import urllib.request
import json


with open("api.key") as api_file:
    API_KEY = api_file.read().strip()

# las_vegas_query = "http://epqs.nationalmap.gov/v1?x=36.1251958&y=-115.3150863&output=json&units=Meters"


# las_vegas_query = "https://epqs.nationalmap.gov/v1/json?x=36&y=-115&wkid=4326&units=Meters&includeDate=false"

some_query = (
    "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536%2C-104.9847034&key="
    + API_KEY
)


# f = urllib.request.urlopen(some_query)

# print(f.read())

# or use requests?
# https://stackoverflow.com/questions/2023893/python-3-get-http-page

import requests

r = requests.get(some_query)

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


import random

for query_index in range(10):
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    q = "https://maps.googleapis.com/maps/api/elevation/json?locations={}%2C{}&key={}".format(
        lat, lng, API_KEY
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


for lat in range(-60, 90, 30):
    for lon in range(180, -180, -30):
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
