import bdgmath

"""
Test to verify haversine functions make sense
"""

lat = 47
lon = -122

for d in range(0, 360, 10):
    n_lat, n_lon = bdgmath.haversine_offset_deg(lat, lon, d, 1.0)

    print(n_lat, n_lon)

    dist = bdgmath.haversine_distance_deg(lat, lon, n_lat, n_lon)
    print("dist:", dist)
