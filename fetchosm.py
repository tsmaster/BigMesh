import os

os.environ["USE_PYGEOS"] = "0"
import geopandas

from pyrosm import get_data

"""
Download OSM data for states to OSM directory

writes: OSM/
"""

fp = get_data("helsinki", directory="OSM")
print("data was downloaded to", fp)

city_names = [
    "Montgomery, Alabama",
    "Juneau, Alaska",
    "Phoenix, Arizona",
    "Little Rock, Arkansas",
    # "Sacramento, California",
    "Denver, Colorado",
    "Hartford, Connecticut",
    "Dover, Delaware",
    "Tallahassee, Florida",
    "Atlanta, Georgia",
    "Honolulu, Hawaii",
    "Boise, Idaho",
    "Springfield, Illinois",
    "Indianapolis, Indiana",
    "Des Moines, Iowa",
    "Topeka, Kansas",
    "Frankfort, Kentucky",
    "Baton Rouge, Louisiana",
    "Augusta, Maine",
    "Annapolis, Maryland",
    "Boston, Massachusetts",
    "Lansing, Michigan",
    "Saint Paul, Minnesota",
    "Jackson, Mississippi",
    "Jefferson City, Missouri",
    "Helena, Montana",
    "Lincoln, Nebraska",
    "Carson City, Nevada",
    "Concord, New Hampshire",
    "Trenton, New Jersey",
    "Santa Fe, New Mexico",
    "Albany, New York",
    "Raleigh, North Carolina",
    "Bismarck, North Dakota",
    "Columbus, Ohio",
    "Oklahoma City, Oklahoma",
    "Salem, Oregon",
    "Harrisburg, Pennsylvania",
    "Providence, Rhode Island",
    "Columbia, South Carolina",
    "Pierre, South Dakota",
    "Nashville, Tennessee",
    "Austin, Texas",
    "Salt Lake City, Utah",
    "Montpelier, Vermont",
    "Richmond, Virginia",
    "Olympia, Washington",
    "Charleston, West Virginia",
    "Madison, Wisconsin",
    "Cheyenne, Wyoming",
]

for n in city_names:
    city, state = n.split(",")

    state = state.strip()
    print("trying to get state", state)
    try:
        fp = get_data(state.strip(), directory="OSM")
        print("data for %s was downloaded to %s" % (n, str(fp)))
    except ValueError as e:
        print("could not get state", e)

country_names = [
    "japan",
    "mexico",
    # "usa",
    "greenland",
    "australia",
    "canada",
    "thailand",
    "north korea",
    "south korea",
    "china",
]

region_names = [
    "northern_california",
    "southern_california",
    "australia_oceania",
    "central_america",
    "south_america",
    "africa",
    "europe",
    "antarctica",
    "madagascar",
    "asia",
]

continents = [
    "north-america",
    "south-america",
    "australia",
]


for r in region_names + country_names + continents:
    print("trying to get region", r)
    try:
        fp = get_data(r, directory="OSM")
        print("data for %s was downloaded to %s" % (r, str(fp)))
    except ValueError as e:
        print("could not get region", e)
