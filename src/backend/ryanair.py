import requests

from models.Country import Country
from models.Airport import Airport
from models.Route import Route
from models.Plan import Plan
from models.Trip import Trip
from models.Flight import Flight


ALL_ROUTES_URL = 'https://services-api.ryanair.com/locate/4/common'
ALL_ROUTES_PARAMS = {'embedded': 'airports'}

ALL_STATIONS_URL = 'https://desktopapps.ryanair.com/v4/res/stations'

ALL_PRICES_URL = 'https://services-api.ryanair.com/farfnd/3/roundTripFares/{}/{}/cheapestPerDay'
ALL_PRICES_PARAMS = {'outboundDateFrom': None, 'outboundDateTo': None, 'inboundDateFrom': None, 'inboundDateTo': None}



def _json_response(url, params=None):
    response = requests.get(url, params=params)
    return response.json()



# JSON response:
#   response = { <iataCode>: info, etc }
#   info = { name: <airportName>, country: <countryCode>, latitude: ..., longitude: ... }
# Return response:
#   reponse = ( countries, airports )
#   countries = { <countryCode>: <Country>, etc }
#   airports = { <iataCode>: <Airport>, etc }
def get_stations_info():
    json = _json_response(ALL_STATIONS_URL)
    countries, airports = {}, {}
    for iataCode, info in json.items():
        if info['country'] not in countries:
            countries[info['country']] = Country(info['country'])
        country = countries[info['country']]
        airport = Airport(country, iataCode, info['name'])
        country.add_airport(airport)
        airports[iataCode] = airport
    return countries, airports



# JSON response:
#   reponse = { airports: [airport, ...] }
#   airport = { iataCode: <iataCode>, name: <airportName>, countryCode: <countryCode>, routes: [route, ...], etc }
#   route = 'city:<cityName>' | 'country:<countryCode>' | 'airport:<iataCode>'
# Return response:
#   airports = { <iataCode>: <Airport>, etc }
def get_all_routes(countries, airports):
    json = _json_response(ALL_ROUTES_URL, ALL_ROUTES_PARAMS)
    for outbound_airport in json['airports']:
        for route in outbound_airport['routes']:
            if _is_airport_route(route):
                if outbound_airport['iataCode'] in airports:
                    _outbound_airport = airports[outbound_airport['iataCode']]
                    _outbound_airport.latitude = outbound_airport['coordinates']['latitude']
                    _outbound_airport.longitude = outbound_airport['coordinates']['longitude']
                else:
                    # Add country to countries
                    if outbound_airport['countryCode'].upper() not in countries:
                        _country = Country(outbound_airport['countryCode'].upper())
                        countries[_country.countryCode] = _country

                    # Add airport to airports + Add airport in corresponding country
                    _country = countries[outbound_airport['countryCode'].upper()]
                    _outbound_airport = Airport(_country, outbound_airport['iataCode'].upper(), outbound_airport['name'])
                    _country.add_airport(_outbound_airport)

                if _extract_iataCode_from_route(route) in airports:
                    _inbound_airport = airports[_extract_iataCode_from_route(route)]

                _outbound_airport.add_route(Route(_outbound_airport, _inbound_airport))
    return countries, airports



# JSON response:
#   response = { 'outbound': info, 'inbound': info }
#   info = { 'fares': [ fare, etc ], 'minFare': ..., 'maxFare': ... }
#   fare = { 'day': 'YYYY-MM-DD', 'soldOut': <Boolean>, 'unavailable': <Boolean>, 'price': price }
#   price = { 'value': <Float>, etc }
# Arguments:
#   outbound_iataCode | inbound_iataCode = <iataCode>
#   outboundDates | inboundDates = ( from, to ) = ( <Date>, <Date> )
# Return response:
#   response = Plan
def get_route_prices(plan, route):
    url = ALL_PRICES_URL.format(route.outbound_airport.iataCode, route.inbound_airport.iataCode)
    params = {  'outboundDateFrom': plan.outboundDateFrom,
                'outboundDateTo': plan.outboundDateTo,
                'inboundDateFrom': plan.inboundDateFrom,
                'inboundDateTo': plan.inboundDateTo
    }

    json = _json_response(url, params)
    for outbound_fare in json['outbound']['fares']:
        if _is_valid_fare(outbound_fare):
            outbound_flight = Flight(route, outbound_fare['day'], outbound_fare['price']['value'])
            for inbound_fare in json['inbound']['fares']:
                if _is_valid_fare(inbound_fare):
                    inbound_flight = Flight(route.return_route, inbound_fare['day'], inbound_fare['price']['value'])
                    plan.add_trip(Trip(outbound_flight, inbound_flight))

    return plan


#################################### UTILS ####################################
import pycountry

# route = 'city:<cityName>' | 'country:<countryCode>' | 'airport:<iataCode>'
def _is_airport_route(route):
    return route.startswith('airport:')

# route = 'airport:<iataCode>'
def _extract_iataCode_from_route(route):
    iataCode = route.split(':')[1]
    if '|' in iataCode:
        iataCode = iataCode.split('|')[0]
    return iataCode

# fare = { 'day': 'YYYY-MM-DD', 'soldOut': <Boolean>, 'unavailable': <Boolean>, 'price': price }
def _is_valid_fare(fare):
    return not fare['soldOut'] and not fare['unavailable']
