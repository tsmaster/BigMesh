import math
import os
import random
import re
import subprocess

from PIL import Image, ImageDraw

import bdgmath

"""
collects city data from state protocol buffer files, 
sorts city by population

reads: OSM/*-latest.osm.pbf
"""

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

# TODO: use capnp state repr, state.py methods

class State:
    def __init__(self, name, osm_filename=None):
        self.name = name.title().replace("-", " ")
        self.abbrev = stateToAbbrevDict[self.name]
        self.osm_filename = osm_filename
        if osm_filename is None:
            self.osm_filename = self.name.lower().replace(" ", "-")

    def __lt__(self, o):
        return self.name < o.name


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


if False:
    states = make_continental_us()
else:
    states = make_sea_to_bos()

rel_path = "OSM"
suffix = "-latest.osm.pbf"

# TODO use proto repr for city, use city.py methods

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