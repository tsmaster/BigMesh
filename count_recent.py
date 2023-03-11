import point

"""
Tool to verify that we don't read too many elevations from Google's
elevation service within 24 hours, to keep monthly use within free use
limits.
"""

pointlist = point.read_pointlist_from_json("points.json")

count = point.count_created_in_recent_hours(24, pointlist)

print("%d in last 24 hours" % count)
