from PIL import Image, ImageDraw

import point

"""
Experiment to visualize point data in points.json
reads: points.json
writes: points.png
"""


scale = 2

im = Image.new("RGBA", (360 * scale, 180 * scale), (0, 0, 0, 0))

draw = ImageDraw.Draw(im)

points = point.read_pointlist_from_json("points.json")

print("drawing %d points" % len(points))

for p in points:
    x = p.lon + 180
    y = 90 - p.lat
    r = 2

    clr = (128, 128, 128)
    if p.elv < 0:
        clr = (100, 100, 200)
    else:
        clr = (100, 200, 100)
    draw.ellipse((x * scale - r, y * scale - r, x * scale + r, y * scale + r), fill=clr)

# im.show()
im.save("points.png")
