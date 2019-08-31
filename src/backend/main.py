from datetime import datetime, timedelta

from ryanair import get_stations_info, get_all_routes, get_route_prices
from models.Plan import Plan
from javascript_gateway import *



def main(start_date, start_gap, return_date, return_gap, origin_countries):
    print('Downloading necessary information !')
    countries, airports = get_stations_info()
    countries, airports = get_all_routes(countries, airports)

    print('Searching for cheapest flights !')
    plan = Plan(countries, start_date, start_gap, return_date, return_gap)
    for country in origin_countries:
        print('Looking at {} airports from country: {} !'.format(len(countries[country].airports), countries[country]))
        for airport in countries[country].airports:
            if len(airport.routes) > 0:
                print('Looking at {} routes from airport: {} !'.format(len(airport.routes), airport))
            else:
                print('There are no routes from airport: {} !'.format(airport))
            for route in airport.routes:
                get_route_prices(plan, route)

    print('Post processing information !')
    airports_locations = format_airports_to_locations(plan.sorted_trips, plan.cheapest_per_airport)
    cheapest_per_country = format_cheapest_per_country(plan.cheapest_per_country)
    json_to_javascript('src/frontend/dynamic/airports.js', 'airports', airports_locations)
    json_to_javascript('src/frontend/dynamic/cheapest_per_country.js', 'cheapest_per_country', cheapest_per_country)



if __name__ == '__main__':
    start_date = datetime.now()
    return_date = datetime.now() + timedelta(days=30)
    start_gap, return_gap = 2, 2
    origin_countries = ['BE']
    main(start_date, start_gap, return_date, return_gap, origin_countries)
