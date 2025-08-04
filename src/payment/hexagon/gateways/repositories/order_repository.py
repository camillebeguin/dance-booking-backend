from typing import Protocol
from payment.hexagon.models.order import Order


class OrderRepository(Protocol):
    def save(self, order: Order): ...
