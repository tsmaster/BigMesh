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
pulls state data from CapnProto states.bin
and outputs them

reads: CapnProto/states.bin
"""

def read_state_protos():
    sp_fn = "ProtoBin/states.bin"
    
    if not (os.path.exists(sp_fn)):
        return {}

    state_dict = {}

    with open(sp_fn, 'rb') as f:
        for state in pr_geog.State.read_multiple(f):
            state_dict[state.abbreviation] = state

    return state_dict


for k,v in read_state_protos().items():
    print("key:", k)
    print(v)
    print()

    
