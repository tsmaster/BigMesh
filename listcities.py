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
pulls city data from CapnProto cities.bin
and outputs them

reads: CapnProto/cities.bin
"""

def read_city_protos():
    cp_fn = "ProtoBin/cities.bin"
    
    if not (os.path.exists(cp_fn)):
        return {}

    city_dict = {}

    with open(cp_fn, 'rb') as f:
        for city in pr_city.City.read_multiple(f):
            city = city.as_builder()
            city_dict[city.idStr] = city

    return city_dict


for k,v in read_city_protos().items():
    print("key:", k)
    print(v)
    print()

    
