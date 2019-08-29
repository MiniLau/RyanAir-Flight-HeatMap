import pycountry


class Country:
    def __init__(self, countryCode):
        self.countryCode = countryCode
        self.name = pycountry.countries.get(alpha_2=countryCode).name
        self._airports = {}


    def add_airport(self, airport):
        self._airports[airport.iataCode] = airport

    def get_airport(self, iataCode):
        return self._airports[iataCode]


    @property
    def airports(self):
        return list(self._airports.values())


    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.countryCode == other.countryCode

    def __hash__(self):
        return hash(self.countryCode)
