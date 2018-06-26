
class Order:

    def __init__(self, quote):
        self.order_id = quote['order_id']
        self.side = quote['side']
        self.price = float(quote['price'])
        self.quantity = int(quote['quantity'])

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def __str__(self):
        return "{} {} {} @ {}".format(self.order_id, self.side, self.quantity, self.price)

