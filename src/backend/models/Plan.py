from datetime import datetime, timedelta



class Plan:
    def __init__(self, all_countries, start_date, start_offset, end_date, end_offset):
        self.all_countries = all_countries
        self._outboundDateFrom = max(start_date - timedelta(days=start_offset), datetime.now())
        self._outboundDateTo = start_date + timedelta(days=start_offset)
        self._inboundDateFrom = max(end_date - timedelta(days=end_offset), self._outboundDateFrom)
        self._inboundDateTo = end_date + timedelta(days=end_offset)

        self.cheapest_per_country = {}
        self.cheapest_per_airport = {}
        self.trips = []


    def add_trip(self, trip):
        self._check_cheapest_per_country(trip)
        self._check_cheapest_per_airport(trip)
        self.trips.append(trip)

    def _check_cheapest_per_country(self, trip):
        destination = trip.destination_country
        if destination not in self.cheapest_per_country or \
                trip.price < self.cheapest_per_country[destination].price:
            self.cheapest_per_country[destination] = trip
    def _check_cheapest_per_airport(self, trip):
        destination = trip.destination_airport
        if destination not in self.cheapest_per_airport or \
                trip.price < self.cheapest_per_airport[destination].price:
            self.cheapest_per_airport[destination] = trip


    @property
    def outboundDateFrom(self):
        return self._outboundDateFrom.strftime('%Y-%m-%d')
    @property
    def outboundDateTo(self):
        return self._outboundDateTo.strftime('%Y-%m-%d')
    @property
    def inboundDateFrom(self):
        return self._inboundDateFrom.strftime('%Y-%m-%d')
    @property
    def inboundDateTo(self):
        return self._inboundDateTo.strftime('%Y-%m-%d')

    @property
    def sorted_trips(self):
        return sorted(self.trips, key=lambda t: t.price)
