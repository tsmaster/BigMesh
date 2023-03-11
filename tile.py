import json
import point


"""
Tile Class with methods
See CapnProto/tile.capnp for serialization
"""


class Tile:
    def __init__(self):
        self.verts_lat_lon = []
        self.centroid_lat_lon = None

        self.tile_id = -1
        self.neighbor_tile_ids = []

        self.city_list = []  # TODO - maybe richer object
        self.state_list = []  # TODO

        self.min_lat = None
        self.max_lat = None
        self.min_lon = None
        self.max_lon = None

    def to_json(self, fn):
        with open(fn, "wt") as f:
            json_str = json.dumps(self.to_dict(), indent=2)
            f.write(json_str)

    def from_json(self, fn):
        with open(fn) as f:
            json_dict = json.loads(f.read())
            self.from_dict(json_dict)

    def to_dict(self):
        out_dict = {}

        # TODO add members

        if self.centroid_lat_lon:
            out_dict["centroid_lat_lon"] = point.point_json_serialize(
                self.centroid_lat_lon
            )

        vert_list = []
        for v in self.verts_lat_lon:
            vert_list.append(point.point_json_serialize(v))
        out_dict["verts_lat_lon"] = vert_list

        out_dict["tile_id"] = self.tile_id

        out_dict["neighbor_tile_ids"] = self.neighbor_tile_ids[:]

        out_dict["city_list"] = self.city_list[:]
        out_dict["state_list"] = self.state_list[:]

        return out_dict

    def from_dict(self, d):
        # TODO initialize from dict d

        self.centroid_lat_lon = point.point_object_hook(d["centroid_lat_lon"])

        vert_list = []
        for obj in d["verts_lat_lon"]:
            v = point.point_object_hook(obj)
            vert_list.append(v)
        self.verts_lat_lon = vert_list

        self.tile_id = d["tile_id"]

        self.neighbor_tile_ids = d["neighbor_tile_ids"]

        self.city_list = d["city_list"]
        self.state_list = d["state_list"]

    def point_in_tile_lat_lon(self, lat, lon):
        if self.min_lat is None:
            self.make_bbox_lat_lon()

        if (
            (lat < self.min_lat)
            or (lat > self.max_lat)
            or (lon < self.min_lon)
            or (lon > self.max_lon)
        ):
            return False

        # todo polygon check

        return True

    def make_bbox_lat_lon(self):
        min_lat = None
        max_lat = None
        min_lon = None
        max_lon = None

        for p in self.verts_lat_lon:
            if min_lat is None:
                min_lat = p.lat
                max_lat = p.lat
                min_lon = p.lon
                max_lon = p.lon
            else:
                min_lat = min(min_lat, p.lat)
                max_lat = max(max_lat, p.lat)
                min_lon = min(min_lon, p.lon)
                max_lon = max(max_lon, p.lon)

        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
