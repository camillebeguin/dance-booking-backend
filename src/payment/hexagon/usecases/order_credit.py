from payment.hexagon.gateways.repositories.order_repository import OrderRepository
from payment.hexagon.models.order import Order


class OrderCreditUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: str, account_id: str):
        order = Order.create(id=order_id, account_id=account_id)
        self.order_repository.save(order)
