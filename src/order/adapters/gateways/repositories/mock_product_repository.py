from order.hexagon.gateways.repositories.product_repository import ProductRepository
from order.hexagon.models.product import Product
from uuid import UUID


class MockProductRepository(ProductRepository):
    def __init__(self):
        self.products = []

    def feed_with(self, products: list[Product]) -> None:
        self.products = products

    def get_by_ids(self, ids: list[UUID]) -> list[Product]:
        return [product for product in self.products if product.id in ids]
