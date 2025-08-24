from uuid import UUID
from order.hexagon.gateways.repositories.order_repository import OrderRepository
from order.hexagon.models.order import Order, OrderItem
from order.hexagon.gateways.repositories.product_repository import ProductRepository


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def execute(self, order_id: str, account_id: str, product_ids: list[UUID]):
        products = self.product_repository.get_by_ids(product_ids)

        items = [
            OrderItem(
                product_id=product.id,
                price=product.current_price,
            )
            for product in products
        ]

        order = Order.create(id=order_id, account_id=account_id, items=items)
        self.order_repository.save(order)
