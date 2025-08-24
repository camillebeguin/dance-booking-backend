from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID
from order.hexagon.models.money import Money


class PaymentStatus(StrEnum):
    init = "init"
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"


@dataclass
class Payment:
    id: UUID
    status: str
    payment_intent_id: str
    amount: Money

    @staticmethod
    def create(order_id: str, payment_intent_id: str, amount: Money) -> "Payment":
        return Payment(
            id=order_id,
            status=PaymentStatus.pending,
            payment_intent_id=payment_intent_id,
            amount=amount,
        )

    def succeed(self):
        self.status = PaymentStatus.succeeded

    def fail(self):
        self.status = PaymentStatus.failed
