class Route:
    def __init__(self, outbound_airport, inbound_airport):
        self.outbound_airport = outbound_airport
        self.inbound_airport = inbound_airport


    @property
    def return_route(self):
        return Route(self.inbound_airport, self.outbound_airport)


    def __repr__(self):
        return '{} --> {}'.format(self.outbound_airport, self.inbound_airport)
