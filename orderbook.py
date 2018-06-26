from order import Order
from ordertree import OrderTree


class OrderBook:
    def __init__(self):
        self.buy_orders = OrderTree()  # Create a separate order tree to maintain all buy orders
        self.sell_orders = OrderTree()  # Create a separate order tree to maintain all sell orders
        self.order_list = dict()  # Create an order list to maintain all (active/completed) orders
        self.all_transactions = list()  # Create a list to store list of all transactions

    def process_limit_order(self, new_order):
        order = Order(new_order)
        print(order)
        self.order_list[order.order_id] = order
        if order.side == 'buy':
            self.buy_orders.insert_order(order)
            while self.sell_orders and order.price >= self.sell_orders.min_price() and order.quantity > 0:
                best_price_asks = self.sell_orders.min_price_list()
                self.do_transactions(self.sell_orders, best_price_asks, order)
            else:
                print('OK')
        elif order.side == 'sell':
            self.sell_orders.insert_order(order)
            while self.buy_orders and order.price <= self.buy_orders.max_price() and order.quantity > 0:
                best_price_bids = self.buy_orders.max_price_list()
                self.do_transactions(self.buy_orders, best_price_bids, order)
            else:
                print('OK')

    def do_transactions(self, order_tree, best_quotes, order):
        while len(best_quotes) > 0 and order.quantity > 0:
            top_order = self.order_list[best_quotes.pop()]
            traded_price = top_order.price
            counter_party = top_order.order_id
            traded_quantity = min(order.quantity, top_order.quantity)
            order.update_quantity(order.quantity - traded_quantity)
            top_order.update_quantity(top_order.quantity - traded_quantity)
            if top_order.quantity > 0:
                best_quotes.append(top_order.order_id)

            if order.side == 'sell':
                transaction_record = {
                    'buy_id': counter_party,
                    'sell_id': order.order_id,
                    'quantity': traded_quantity,
                    'price': traded_price
                }
            else:
                transaction_record = {
                    'buy_id': order.order_id,
                    'sell_id': counter_party,
                    'quantity': traded_quantity,
                    'price': traded_price
                }
            self.all_transactions.append(transaction_record)
        if not len(best_quotes):
            order_tree.remove_price(order.price)

    def cancel_order(self, order):
        if order.side == 'buy':
            self.buy_orders.remove_order(order)
        else:
            self.sell_orders.remove_order(order)
        del self.order_list[order.order_id]
        del order
        print('OK')

