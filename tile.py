import json


class Tile:
    def __init__(self):
        pass


    def to_json(self, fn):
        with open(fn, 'wt') as f:
            json_str = json.dumps(self.to_dict(), indent=2)
            f.write(json_str)


    def from_json(self, fn):
        with open(fn) as f:
            json_dict = json.loads(f.read())
            self.from_dict(json_dict)

    def to_dict(self):
        out_dict = {}


        # TODO add members

        return out_dict

    def from_dict(self, d):

        # TODO initialize from dict d

        pass

    
