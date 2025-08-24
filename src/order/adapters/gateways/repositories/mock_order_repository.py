from order.hexagon.gateways.repositories.order_repository import OrderRepository
from order.hexagon.models.order import Order


class MockOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = []

    def feed_with(self, orders: list[Order]):
        self.orders = orders

    def save(self, order: Order):
        existing_order = next((o for o in self.orders if o.id == order.id), None)
        if existing_order:
            self.orders[self.orders.index(existing_order)] = order
        else:
            self.orders.append(order)

    def get_by_id(self, order_id: str) -> Order:
        return next(order for order in self.orders if order.id == order_id)
