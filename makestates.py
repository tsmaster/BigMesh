import glob
import math
import os
import random
import re
import subprocess
import sys

from PIL import Image, ImageDraw

import capnp
import CapnProto.geog_capnp as pr_geog

import bdgmath
import city

"""
collects state data from state protocol buffer files, 
writes to CapnProto protocol buffers

reads: OSM/*-latest.osm.pbf
writes: ProtoBin/states.bin
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


osm_rel_path = "OSM"
osm_suffix = "-latest.osm.pbf"



def make_state_proto_filenames(statename):
    statename = statename.lower()
    statenames = [statename]

    if statename == 'california':
        statenames = ['norcal', 'socal']

    fns = []

    for sn in statenames:
        sn = sn.replace(' ', '-')
        p = os.path.join(osm_rel_path, sn + osm_suffix)

        fns.append(p)

        
    return fns
    

# TODO: use capnp state repr, state.py methods

class State:
    def __init__(self, name, osm_filename=None):
        self.name = name.title().replace("-", " ")
        if self.name in stateToAbbrevDict:
            self.abbrev = stateToAbbrevDict[self.name]
            self.country_name = 'United States of America'
        else:
            self.abbrev = self.name
            self.country_name = self.name
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
        #"montana",
        #"north-dakota",
        #"minnesota",
        #"wisconsin",
        #"illinois",
        #"indiana",
        #"ohio",
        #"pennsylvania",
        #"new-york",
        #"massachusetts"
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


if len(sys.argv) > 1:
    states = []
    for a in sys.argv[1:]:
        for g in glob.glob(a):
            print("found",g)
            fn = os.path.split(g)[1]
            print("filename:", fn)
            hyph_idx = fn.rindex('-')
            loc_name = fn[:hyph_idx]
            print("base:", loc_name)
            
            s = State(loc_name, loc_name)
            states.append(s)
            
else:
    if False:
        states = make_continental_us()
    else:
        states = make_sea_to_bos()

rel_path = "OSM"
suffix = "-latest.osm.pbf"

# TODO use proto repr for city, use city.py methods

class City:
    def __init__(self, name, state_name, country_name, pop, vertid):
        self.name = name
        self.state_name = state_name
        self.country_name = country_name
        self.pop = pop
        self.vertid = vertid
        self.city_id = city.make_city_id(name, state_name, country_name)

    def __lt__(self, o):
        return self.pop < o.pop

    def __str__(self):
        return "%s, %s p: %d v: %d cid: %s" % (
            self.name,
            self.state_name,
            self.pop,
            self.vertid,
            self.city_id
        )

    def __repr__(self):
        return str(self)
    

cities = []
verts = []

def read_state_protos():
    sp_fn = "ProtoBin/states.bin"
    
    if not (os.path.exists(sp_fn)):
        return {}

    state_dict = {}

    with open(sp_fn, 'rb') as f:
        for state in pr_geog.State.read_multiple(f):
            state_dict[state.abbreviation] = state

    return state_dict

def write_state_protos(d):
    sp_fn = "ProtoBin/states.bin"

    with open(sp_fn, 'wb') as f:
        for k,v in d.items():
            print("writing", k)
            v.write(f)
            
def make_states():
    sd = {}
    for state_name, state_abbrev in stateToAbbrevDict.items():
        print("state: {} ({})".format(state_name, state_abbrev))

        fns = make_state_proto_filenames(state_name)

        print("files:", fns)

        min_lat, max_lat, min_lon, max_lon = None, None, None, None
        
        for f_idx, f in enumerate(fns):
            assert(os.path.exists(f))

            # get bbox
            
            cmd = "./CalcBBox/calcbbox/target/release/calcbbox " + f
            print(cmd)

            proc = subprocess.run(cmd.split(), capture_output=True)

            print("returncode:", proc.returncode)

            if proc.returncode == 0:
                out_lines = str(proc.stdout, "UTF-8").split("\n")
                #print("lines:", out_lines)

                lats = out_lines[5].strip().split()
                lons = out_lines[6].strip().split()

                print ("lats", lats)
                print ("lons", lons)

                if f_idx == 0:
                    min_lat = float(lats[1])
                    max_lat = float(lats[2])
                    min_lon = float(lons[1])
                    max_lon = float(lons[2])
                else:
                    min_lat = min(min_lat, float(lats[1]))
                    max_lat = max(max_lat, float(lats[2]))
                    min_lon = min(min_lon, float(lons[1]))
                    max_lon = max(max_lon, float(lons[2]))

        bbox = pr_geog.BBoxDeg.new_message()
        bbox.minLon = min_lon
        bbox.minLat = min_lat
        bbox.maxLon = max_lon
        bbox.maxLat = max_lat

        print("bbox:", bbox)

        s = pr_geog.State.new_message()

        s.id = len(sd) + 1
        s.name = state_name
        s.abbreviation = state_abbrev
        s.countryId = 'USA'
        s.bboxDeg = bbox
        sd[s.abbreviation] = s

    return sd


sd = make_states()

write_state_protos(sd)

sd = read_state_protos()

for s_key, s in sd.items():
    print(s_key)
    print(s)
    print()

exit(-1)

            
    

state_protos = read_state_protos()
city_protos = read_city_protos()
vert_protos = readd_vert_protos()


for s in states:
    print("state: %s (%s), %s" % (s.name, s.abbrev, s.country_name))

    if s.country_name == "United States of America":
        print ("is state")
        
    # fp = get_data(s, directory=rel_path)

    p = os.path.join(rel_path, s.osm_filename + suffix)

    print(p)

    cmd = "./target/release/get_cities " + p
    print(cmd)

    proc = subprocess.run(cmd.split(), capture_output=True)

    print("returncode:", proc.returncode)

    out_lines = str(proc.stdout, "UTF-8").split("\n")

    if proc.returncode == 0:
        for line in out_lines:
            #print(line)
            if line.startswith("Found a city:"):
                # print(line)
                m = re.search(
                    'name="(.+)" population=([0-9]+) vertexid=([0-9]+)',
                    line,
                )
                # print ("city match?", m)
                if m:
                    #print(m[1])
                    #print(m[2])
                    #print(m[3])

                    name = m[1]
                    pop = int(m[2])
                    vertid = int(m[3])

                    city_obj = City(name, s.name, s.country_name, pop, vertid)
                    for c in city_obj.city_id:
                        if c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                            print("parsing", name)
                            print("bad char:", c)
                            exit(-1)
                    cities.append(city_obj)
                    print("city:", city_obj)
            elif line.startswith("vertex id:"):
                #print(line)
                m = re.search(
                    'id: ([0-9]+) lon: ([0-9\.-]*) lat: ([0-9\.-]*)', line)
                if m:
                    #print(m[1])
                    #print(m[2])
                    #print(m[3])

                    vertid = int(m[1])
                    vertlon = float(m[2])
                    vertlat = float(m[3])

                    v = (vertid, vertlon, vertlat)
                    print("vert:", v)
                    verts.append(v)
                else:
                    print("no match!!")

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

print()
verts.sort()
for v in verts:
    print(v)
