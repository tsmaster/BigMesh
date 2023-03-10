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
import CapnProto.city_capnp as pr_city
import CapnProto.vertex_capnp as pr_vertex

import bdgmath
import city
import country

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
    if True:
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
            state_dict[state.abbreviation] = state.as_builder()

    return state_dict

def write_state_protos(d):
    sp_fn = "ProtoBin/states.bin"

    with open(sp_fn, 'wb') as f:
        for k,v in d.items():
            print("writing state", k)
            v.write(f)



def read_city_protos():
    cp_fn = "ProtoBin/cities.bin"
    
    if not (os.path.exists(cp_fn)):
        return {}

    city_dict = {}

    with open(cp_fn, 'rb') as f:
        for city in pr_city.City.read_multiple(f):
            city_dict[city.idStr] = city.as_builder()

    return city_dict

def write_city_protos(d):
    cp_fn = "ProtoBin/cities.bin"

    with open(cp_fn, 'wb') as f:
        for k,v in d.items():
            print("writing city", k)
            print(type(v), v)
            v.clear_write_flag()            
            v.write(f)


# TODO more kinds of vertices

def read_vert_protos():
    vp_fn = "ProtoBin/verts_city.bin"
    
    if not (os.path.exists(vp_fn)):
        return {}

    vert_dict = {}

    with open(vp_fn, 'rb') as f:
        for vert in pr_vertex.Vertex.read_multiple(f):
            vert_dict[(vert.desc.id, vert.desc.source)] = vert.as_builder()

    return vert_dict

def write_vert_protos(d):
    vp_fn = "ProtoBin/verts_city.bin"

    with open(vp_fn, 'wb') as f:
        for k,v in d.items():
            print("writing vert", k)
            v.write(f)

state_protos = read_state_protos()
city_protos = read_city_protos()
vert_protos = read_vert_protos()

cities_by_state = {} # dictionary mapping from state abbrev to list of city ids

if not state_protos:
    print("ProtoBin/states.bin must exist.")
    print("run makestates.py to generate it.")
    exit(-1)


for s in states:
    print("state: %s (%s), %s" % (s.name, s.abbrev, s.country_name))

    state_proto_obj = None
    state_city_abbrevs = []
    
    if s.country_name == "United States of America":
        print ("is state")
        state_proto_obj = state_protos[s.abbrev]

        print("found state proto obj")
        print(state_proto_obj)
        state_city_abbrevs = [x for x in state_proto_obj.cityIds]
    else:
        print("not a state")

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
                    for nc in city_obj.city_id:
                        if nc not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                            print("parsing", name)
                            print("bad char:", nc)
                            exit(-1)

                    if not (city_obj.city_id in city_protos):
                        city_proto_obj = pr_city.City.new_message()
                        city_proto_obj.id = len(city_protos) + 1
                        city_proto_obj.name = name
                        city_proto_obj.idStr = city_obj.city_id
                        if state_proto_obj:
                            city_proto_obj.state = state_proto_obj.abbreviation
                        city_proto_obj.country = country.get_country_id(s.country_name)

                        v = pr_vertex.VertDesc.new_message()
                        v.id = vertid
                        v.source = pr_vertex.VertDesc.Source.osm
                        city_proto_obj.positionVertex = v

                        city_proto_obj.population = pop
                    
                        cities.append(city_obj)
                        city_protos[city_obj.city_id] = city_proto_obj
                        print("city:", city_obj)
                        print("city_proto_obj:", city_proto_obj)
                        if city_obj.city_id not in state_city_abbrevs:
                            state_city_abbrevs.append(city_obj.city_id)
                            state_city_abbrevs.sort()
                    else:
                        print("{} already exists".format(city_obj.city_id))
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

                    # TODO see if vert already exists

                    vert_desc = pr_vertex.VertDesc.new_message()
                    vert_desc.id = vertid
                    vert_desc.source = pr_vertex.VertDesc.Source.osm

                    v_tag = (vert_desc.id, vert_desc.source)

                    if (not (v_tag in vert_protos)):
                        vert_obj = pr_vertex.Vertex.new_message()
                        vert_obj.desc = vert_desc
                        vert_obj.lonDeg = vertlon
                        vert_obj.latDeg = vertlat
                        
                        vert_protos[v_tag] = vert_obj
                        print("adding vert obj:", vert_obj)
                    else:
                        print("vert tag {} already in dict".format(v_tag))
                else:
                    print("no match!!")

        if state_proto_obj:
            print("adding cities {} to {}".format(
                state_city_abbrevs, state_proto_obj.abbreviation))
            state_proto_obj.cityIds = state_city_abbrevs

    else:
        print("error")
        err_lines = str(proc.stderr, "UTF-8").split("\n")
        for e in err_lines:
            print("ERR:  ", e)

write_state_protos(state_protos)            
write_city_protos(city_protos)
write_vert_protos(vert_protos)
