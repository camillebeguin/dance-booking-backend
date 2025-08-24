from typing import Protocol
from uuid import UUID
from order.hexagon.models.product import Product


class ProductRepository(Protocol):
    def get_by_ids(self, ids: list[UUID]) -> list[Product]: ...
