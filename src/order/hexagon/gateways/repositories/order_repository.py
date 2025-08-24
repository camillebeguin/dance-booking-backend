from typing import Protocol
from order.hexagon.models.order import Order


class OrderRepository(Protocol):
    def save(self, order: Order): ...

    def get_by_id(self, order_id: str) -> Order: ...
