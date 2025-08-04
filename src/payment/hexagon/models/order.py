from dataclasses import dataclass
from uuid import UUID
from enum import StrEnum


class OrderStatus(StrEnum):
    started = "started"


@dataclass
class Order:
    id: UUID
    account_id: UUID
    status: OrderStatus

    @staticmethod
    def create(id: UUID, account_id: UUID):
        return Order(id=id, account_id=account_id, status=OrderStatus.started)
