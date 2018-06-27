from order import Order
from ordertree import OrderTree


class OrderBook:

    def __init__(self):

        self.buy_orders = OrderTree()  # Create a separate order tree to maintain all unfilled buy orders
        self.sell_orders = OrderTree()  # Create a separate order tree to maintain all unfilled sell orders
        self.order_list = dict()  # Create an order list to maintain all (active/completed) orders
        self.all_transactions = list()  # Create a list to store list of all transactions

    def process_limit_order(self, new_order):

        order = Order(new_order)  # Create a new object for the latest order
        self.order_list[order.order_id] = order  # Make an entry in the order list

        # try to fill the order from the standing counter-parties
        if order.side == 'buy':
            while self.sell_orders and order.price >= self.sell_orders.min_price() and order.quantity:
                self.do_same_price_transactions(self.sell_orders, self.sell_orders.min_price_quotes(), order)
            # if the order is still unfilled make an entry in the buy tree
            if order.quantity:
                self.buy_orders.insert_order(order)

        else:
            while self.buy_orders and order.price <= self.buy_orders.max_price() and order.quantity:
                self.do_same_price_transactions(self.buy_orders, self.buy_orders.max_price_quotes(), order)
            # if the order is still unfilled make an entry in the sell tree
            if order.quantity:
                self.sell_orders.insert_order(order)

    def do_same_price_transactions(self, order_tree, best_quotes, order):

        while len(best_quotes) and order.quantity:
            top_order = self.order_list[best_quotes.pop()]
            traded_quantity = min(order.quantity, top_order.quantity)
            order.update_quantity(order.quantity - traded_quantity)
            top_order.update_quantity(top_order.quantity - traded_quantity)
            if top_order.quantity:
                best_quotes.append(top_order.order_id)

            if order.side == 'sell':
                transaction_record = {
                    'buy_id': top_order.order_id,
                    'sell_id': order.order_id,
                    'quantity': traded_quantity,
                    'price': top_order.price
                }
            else:
                transaction_record = {
                    'buy_id': order.order_id,
                    'sell_id': top_order.order_id,
                    'quantity': traded_quantity,
                    'price': top_order.price
                }
            self.all_transactions.append(transaction_record)

        if len(best_quotes) == 0:
            order_tree.remove_price(order.price)

    def cancel_order(self, order):

        if order.side == 'buy':
            self.buy_orders.remove_order(order)
        else:
            self.sell_orders.remove_order(order)
        del self.order_list[order.order_id]
        del order
        print('OK')

