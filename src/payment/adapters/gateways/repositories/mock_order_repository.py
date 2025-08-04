from payment.hexagon.gateways.repositories.order_repository import OrderRepository
from payment.hexagon.models.order import Order


class MockOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = []

    def feed_with(self, orders: list[Order]):
        self.orders = orders

    def save(self, order: Order):
        if order.id in self.orders:
            self.orders[self.orders.index(order)] = order
        else:
            self.orders.append(order)
