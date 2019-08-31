class Airport:
    def __init__(self, country, iataCode, name):
        self.country = country
        self.iataCode = iataCode
        self.name = name
        self.latitude, self.longitude = 0, 0
        self._routes = {}


    def add_route(self, route):
        self._routes[route.inbound_airport] = route


    @property
    def routes(self):
        return list(self._routes.values())


    def __repr__(self):
        return '{} ({})'.format(self.name, self.country)

    def __eq__(self, other):
        return self.iataCode == other.iataCode

    def __hash__(self):
        return hash(self.iataCode)
