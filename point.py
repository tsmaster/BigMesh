import math
import datetime
import json


class Point:
    def __init__(self, lat, lon, elv, creation_time):
        self.lat = lat  # north/south
        self.lon = lon  # east/west
        self.elv = elv  # in meters
        self.creation_time = creation_time
        if not creation_time:
            self.creation_time = datetime.datetime.now()

    def dist(self, o):
        d_lat = abs(self.lat - o.lat)
        d_lon = abs(self.lon - o.lon)

        if d_lon > 180:
            d_lon -= 180

        return math.sqrt(d_lat * d_lat + d_lon * d_lon)

    def __lt__(self, o):
        return (self.lon, self.lat) < (o.lon, o.lat)

    def __str__(self):
        if self.elv:
            return "Lat,Lon:(%f,%f)E:%f" % (self.lat, self.lon, self.elv)
        else:
            return "Lat,Lon:(%f,%f)" % (self.lat, self.lon)

    def __repr__(self):
        return str(self)


def point_json_serialize(obj):
    if isinstance(obj, Point):
        p_dir = {}
        p_dir["lat"] = obj.lat
        p_dir["lon"] = obj.lon
        if obj.elv:
            p_dir["elv"] = obj.elv
        p_dir["created"] = obj.creation_time.isoformat()
        p_dir["type"] = "Point"
        return p_dir
    raise TypeError("Type %s not serializable" % type(obj))


def point_object_hook(dct):
    if ("type" in dct) and (dct["type"] == "Point"):
        cd_str = dct["created"]
        cd_dt = datetime.datetime.fromisoformat(cd_str)
        if "elv" in dct:
            elv = dct["elv"]
        else:
            elv = None
        return Point(dct["lat"], dct["lon"], elv, cd_dt)
    return dct


def write_pointlist_to_json(filename, pointlist):
    with open(filename, "wt") as f:
        f.write(
            json.dumps(
                pointlist, sort_keys=True, indent=2, default=point_json_serialize
            )
        )


def read_pointlist_from_json(filename):
    with open(filename, "rt") as f:
        data = f.read()
        return json.loads(data, object_hook=point_object_hook)


def count_created_in_recent_hours(hour_count, pointlist):
    count = 0

    ref_delta = datetime.timedelta(hours=hour_count)
    for p in pointlist:
        td = datetime.datetime.now() - p.creation_time
        # print("td:", td)
        if td < ref_delta:
            count += 1

    return count
