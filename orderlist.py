class OrderList(object):

    def __init__(self):
        self.top_order = None
        self.tail_order = None
        self.last = None
        self.length = 0

    def __len__(self):
        return self.length

    def __iter__(self):
        self.last = self.top_order
        return self

    def __next__(self):
        if self.last is None:
            raise StopIteration
        else:
            return_value = self.last
            self.last = self.last.next_order
            return return_value

    def append_order(self, order):
        if len(self) == 0:
            order.next_order = None
            order.prev_order = None
            self.top_order = order
            self.tail_order = order
        else:
            order.prev_order = self.tail_order
            order.next_order = None
            self.tail_order.next_order = order
            self.tail_order = order
        self.length += 1

    def remove_order(self, order):
        self.length -= 1
        if len(self) == 0:
            return
        next_order = order.next_order
        prev_order = order.prev_order
        if next_order is not None and prev_order is not None:
            next_order.prev_order = prev_order
            prev_order.next_order = next_order
        elif next_order is not None:
            next_order.prev_order = None
            self.top_order = next_order
        elif prev_order is not None:
            prev_order.next_order = None
            self.tail_order = prev_order

