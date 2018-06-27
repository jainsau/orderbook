import csv
from orderbook import OrderBook

# Create an order book to maintain active orders
order_book = OrderBook()

with open('trades.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['side'] == 'cancel':
            print("{} {}".format(row['side'], row['order_id']))
            if row['order_id'] in order_book.order_list:
                order = order_book.order_list[row['order_id']]
                if order.quantity:
                    order_book.cancel_order(order)
                else:
                    print('Failed - already fully filled')
            else:
                print('Failed – no such active order')
        else:
            print("{} {} {} @ {}".format(row['order_id'], row['side'], row['quantity'], row['price']))
            order_book.process_limit_order(row)

