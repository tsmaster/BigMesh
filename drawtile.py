import os
import sys

import city
import state

"""
Demo 0
Draw a tile, containing all info within
  tile boundaries
  national boundaries
  city boundaries
  city center points
  highways
  land polygons
  water body polygons
    oceans
    lakes
    rivers

TODO
reads: ???
writes: ???
"""

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # hope that we can find a unique city
        city_name = sys.argv[1]
        state_name = None
        country_name = None
        
    elif len(sys.argv) == 3:
        city_name = sys.argv[1]
        state_name = sys.argv[2]
        country_name = None


    city_list = city.get_cities(city_name, state_name, country_name)

    if len(city_list) == 0:
        print("no cities found by name", sys.argv[1])
        exit(-1)

    if len(city_list) > 1:
        print("multiple matches:")
        for c in city_list:
            print (c)
        exit(-1)

    print ("found city", sys.argv[1])
    print (city_list[0])
    exit(0)


