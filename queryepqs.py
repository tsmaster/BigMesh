import urllib.request

#las_vegas_query = "http://epqs.nationalmap.gov/v1?x=36.1251958&y=-115.3150863&output=json&units=Meters"


las_vegas_query = "https://epqs.nationalmap.gov/v1/json?x=36&y=-115&wkid=4326&units=Meters&includeDate=false"

f = urllib.request.urlopen(las_vegas_query)

print(f.read())


# or use requests?
# https://stackoverflow.com/questions/2023893/python-3-get-http-page
"""
import requests

r = requests.get(las_vegas_query)
for line in r:
    print(line.strip())
"""
