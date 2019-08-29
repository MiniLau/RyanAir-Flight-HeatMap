class Flight:
    def __init__(self, route, date, price):
        self.route = route
        self.date = date
        self.price = price


    def __repr__(self):
        return '{} | {}€ | {}'.format(date, price, route)
