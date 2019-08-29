from datetime import datetime, timedelta



class Plan:
    def __init__(self, all_countries, start_date, start_offset, end_date, end_offset):
        self.all_countries = all_countries
        self._outboundDateFrom = max(start_date - timedelta(days=start_offset), datetime.now())
        self._outboundDateTo = start_date + timedelta(days=start_offset)
        self._inboundDateFrom = max(end_date - timedelta(days=end_offset), self._outboundDateFrom)
        self._inboundDateTo = end_date + timedelta(days=end_offset)

        self.cheapest_per_country = {}
        self.trips = []


    def add_trip(self, trip):
        dest_countryCode = trip.destination_country.countryCode
        if dest_countryCode not in self.cheapest_per_country or \
                trip.price < self.cheapest_per_country[dest_countryCode].price:
            self.cheapest_per_country[dest_countryCode] = trip

        self.trips.append(trip)


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
