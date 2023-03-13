import state
import country

"""
City class (methods, not serialization)
See also CapnProto/city.capnp

"""


class City:
    def __init__(self, latlon, name, state_name, tile_id, population = None, elevation = None):
        self.latlon = latlon
        self.name = name
        self.state_name = state_name,
        self.tile_id = tile_id,
        self.population = population
        self.elevation = elevation

rewrite_chars = {
    'Ñ': 'N'
}

def make_city_id(city_name, state_name, country_name):
    if state_name:
        state_id = state.get_state_id(state_name)
    else:
        state_id = None
        
    country_id = country.get_country_id(country_name)

    out = country_id + '_'
    if state_id:
        out = out + state_id + '_'
    city_name = city_name.upper()
    
    out += city_name[0]
    city_name = city_name[1:]
    for c in city_name:
        if c in "AEIOU '’-.()ÁÈÉÍÓÔŎÚ":
            continue
        if c in rewrite_chars.keys():
            c = rewrite_chars[c]
        if c == out[-1]:
            continue
        out = out + c

    return out

def get_cities_by_city(city_name):
    return []

def get_cities_by_city_state(city_name, state_id):
    return []

def get_cities(city_name, state_id, country_id):
    if state_id is None:
        return get_cities_by_city(city_name)
    else:
        return get_cities_by_city_state(city_name, state_id)

    
if __name__ == '__main__':
    city_list = [("Seattle", "Washington"),
                 ("Yakima", "Washington"),
                 ("Boise", "Idaho"),
                 ("Boston", "Massachusetts")]

    for city_pair in city_list:
        city_name, state_name = city_pair
        city_id = make_city_id(city_name, state_name)
        print(city_name, state_name, city_id)
