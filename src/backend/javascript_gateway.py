import json, os



def _json_to_javascript(path, variable_name, dic):
    with open(path, 'w') as f:
        content = 'var {} = JSON.parse(\'{}\');'.format(variable_name, json.dumps(dic))
        f.write(content)



# Countries JSON:
#   reponse = { <Int>: info }
#   info = { 'lat': ..., 'lng': ..., 'name': ..., 'countryCode': ..., 'hide': 'yes' }
def format_airports_to_locations(sorted_trips, cheapest_per_airport):
    airports, formatted, count = {}, {}, 0
    for trip in sorted_trips:
        if trip.destination_airport not in airports:
            airports[trip.destination_airport] = count
            formatted[count] = _format_airport_to_location(trip.destination_airport, cheapest_per_airport)
            count += 1
        index = airports[trip.destination_airport]
        formatted[index] = _append_description_to_location(formatted[index], trip)
    return formatted

def _format_airport_to_location(airport, cheapest_per_airport):
    min_price = cheapest_per_airport[airport].price
    return {
        'lat': airport.latitude, 'lng': airport.longitude,
        'countryCode': airport.country.countryCode, 'hide': 'yes',
        'name': '{} (min. {}€)'.format(airport.name, min_price),
        '_description': []
    };

def _append_description_to_location(content, trip):
    if len(content['_description']) < 10:
        content['_description'].append(('{}€'.format(trip.price), '{} days'.format(trip.duration), repr(trip.orgigin_airport)))
    return content


# Cheapest_per_country JSON:
#   response = { key: info }
#   info = { 'price': <Float> }
def format_cheapest_per_country(cheapest_per_country):
    formatted = {}
    for country, trip in cheapest_per_country.items():
        formatted[country.countryCode] = { 'price': trip.price }
    return formatted



if __name__ == '__main__':
    from ryanair import get_stations_info, get_all_routes, get_route_prices
    from models.Plan import Plan
    from datetime import datetime, timedelta

    print('Downloading necessary information !')
    countries, airports = get_stations_info()
    countries, airports = get_all_routes(countries, airports)

    print('Searching for cheapest flights !')
    plan = Plan(countries, datetime.now() + timedelta(days=20), 2, datetime.now() + timedelta(days=30), 2)
    for airport in countries['BE'].airports:
        if len(airport.routes) > 0:
            print('Looking at {} routes from airport: {} !'.format(len(airport.routes), airport))
        else:
            print('There are no routes from airport: {} !'.format(airport))
        for route in airport.routes:
            get_route_prices(plan, route)

    print('Post processing information !')
    airports_locations = format_airports_to_locations(plan.sorted_trips, plan.cheapest_per_airport)
    cheapest_per_country = format_cheapest_per_country(plan.cheapest_per_country)
    _json_to_javascript('src/frontend/dynamic/airports.js', 'airports', airports_locations)
    _json_to_javascript('src/frontend/dynamic/cheapest_per_country.js', 'cheapest_per_country', cheapest_per_country)
