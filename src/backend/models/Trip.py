class Trip:
    def __init__(self, outbound_flight, return_flight):
        self.outbound_flight = outbound_flight
        self.return_flight = return_flight


    @property
    def price(self):
        return round(self.outbound_flight.price + self.return_flight.price, 2)
    @property
    def duration(self):
        return (self.return_flight.date - self.outbound_flight.date).days


    @property
    def origin_country(self):
        return self.outbound_flight.route.outbound_airport.country
    @property
    def destination_country(self):
        return self.outbound_flight.route.inbound_airport.country

    @property
    def orgigin_airport(self):
        return self.outbound_flight.route.outbound_airport
    @property
    def destination_airport(self):
        return self.outbound_flight.route.inbound_airport


    def __repr__(self):
        return '({} days) | {}€ | From: {}'.format(self.duration, self.price, self.orgigin_airport)
