from dataclasses import dataclass
from uuid import UUID
from order.hexagon.models.money import Money


@dataclass
class Product:
    id: UUID
    current_price: Money
