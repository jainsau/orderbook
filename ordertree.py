from sortedcontainers import SortedDict
from collections import deque


class OrderTree:

    def __init__(self):
        self.price_map = SortedDict()
        self.prices = self.price_map.keys()

    def __len__(self):
        return len(self.prices)

    def create_price(self, price):
        self.price_map[price] = deque()

    def remove_price(self, price):
        del self.price_map[price]

    def insert_order(self, order):
        if order.price not in self.prices:
            self.create_price(order.price)
        self.price_map[order.price].appendleft(order.order_id)

    def remove_order(self, order):
        self.price_map[order.price].remove(order.order_id)
        if len(self.price_map[order.price]) == 0:
            self.remove_price(order.price)

    def min_price(self):
        if len(self):
            return self.prices[0]
        else:
            return None

    def max_price(self):
        if len(self):
            return self.prices[-1]
        else:
            return None

    def get_quotes_list(self, price):
        if price in self.prices:
            return self.price_map[price]
        else:
            return None

    def min_price_quotes(self):
        return self.get_quotes_list(self.min_price())

    def max_price_quotes(self):
        return self.get_quotes_list(self.max_price())

