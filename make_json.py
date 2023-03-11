import datetime
import json

import point

points = []

"""
converts points.txt into points.json
reads: points.txt
writes: points.json
"""

def json_serial(obj):
    if isinstance(obj, point.Point):
        p_dir = {}
        p_dir["lat"] = obj.lat
        p_dir["lon"] = obj.lon
        p_dir["elv"] = obj.elv
        p_dir["created"] = obj.creation_time.isoformat()
        p_dir["type"] = "Point"
        return p_dir
    raise TypeError("Type %s not serializable" % type(obj))


with open("points.txt") as pf:
    lat = 0
    lon = 0
    elv = 0

    old_time = datetime.datetime(2023, 1, 9, 12, 0)

    for line_num, line in enumerate(pf.readlines()):
        line = line.strip()

        lm = line_num % 4

        if lm == 3:
            pt = point.Point(lat, lon, elv, old_time)
            points.append(pt)

        else:
            terms = line.split(":")
            val = float(terms[1].strip())
            if terms[0] == "lat":
                lat = val
            elif terms[0] == "lon":
                lon = val
            elif terms[0] == "elv":
                elv = val
            else:
                print("unknown line:", line)
                assert False

print(json.dumps(points, sort_keys=True, indent=2, default=json_serial))

point.write_pointlist_to_json("points.json", points)

# gen_2_points = point.read_pointlist_from_json('points.json')
# point.write_pointlist_to_json('points_2.json', gen_2_points)
