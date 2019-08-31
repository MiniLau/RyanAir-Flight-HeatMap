from datetime import datetime


class Flight:
    def __init__(self, route, date_str, price):
        self.route = route
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.price = price


    def __repr__(self):
        return '{} | {}€ | {}'.format(date, price, route)
