from dataclasses import dataclass
from uuid import UUID, uuid4
from enum import StrEnum
from order.hexagon.models.money import Money
from order.hexagon.models.exceptions import OrderAlreadyConfirmedException
from order.hexagon.models.event import DomainEvent


class OrderStatus(StrEnum):
    started = "started"
    confirmed = "confirmed"
    completed = "completed"
    failed = "failed"


class OrderEventType(StrEnum):
    order_completed = "order_completed"


@dataclass
class OrderItem:
    product_id: UUID
    price: Money


@dataclass
class Order:
    id: UUID
    account_id: UUID
    status: OrderStatus
    items: list[OrderItem]

    @property
    def total_amount(self) -> Money:
        total_amount = Money(amount=0, currency=self.items[0].price.currency)

        for item in self.items:
            total_amount += item.price

        return total_amount

    @staticmethod
    def create(id: UUID, account_id: UUID, items: list[OrderItem]):
        return Order(
            id=id, account_id=account_id, status=OrderStatus.started, items=items
        )

    def confirm(self):
        if self.status == OrderStatus.confirmed:
            raise OrderAlreadyConfirmedException

        self.status = OrderStatus.confirmed

    def complete(self):
        self.status = OrderStatus.completed
        return DomainEvent(
            id=str(uuid4()),
            type=OrderEventType.order_completed,
            data={"order_id": self.id},
        )

    def fail(self):
        self.status = OrderStatus.failed
