from uuid import UUID
from typing import Protocol
from order.hexagon.models.payment import Payment


class PaymentRepository(Protocol):
    def save(self, payment: Payment) -> None: ...

    def find_by_order_id(self, order_id: UUID) -> Payment | None: ...

    def find_by_payment_intent_id(self, payment_intent_id: str) -> Payment | None: ...
