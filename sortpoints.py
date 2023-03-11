import math

"""
experiment to sort points.txt
reads: points.txt
"""

class Point:
    def __init__(self, lat, lon, elv):
        self.lat = lat
        self.lon = lon
        self.elv = elv

    def dist(self, o):
        d_lat = abs(self.lat - o.lat)
        d_lon = abs(self.lon - o.lon)

        if d_lon > 180:
            d_lon -= 180

        return math.sqrt(d_lat * d_lat + d_lon * d_lon)

    def __lt__(self, o):
        return (self.lon, self.lat) < (o.lon, o.lat)


points = []

with open("points.txt") as pf:
    lat = 0
    lon = 0
    elv = 0

    for line_num, line in enumerate(pf.readlines()):
        line = line.strip()

        lm = line_num % 4

        if lm == 3:
            pt = Point(lat, lon, elv)
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

new_points = []

TOO_CLOSE = 0.5

for p in points:
    found_close = False
    for np in new_points:
        d = np.dist(p)
        if d < TOO_CLOSE:
            found_close = True
            break
    if not found_close:
        new_points.append(p)

new_points.sort()

for pi, p in enumerate(new_points):
    print(pi, p.lat, p.lon, p.elv)
