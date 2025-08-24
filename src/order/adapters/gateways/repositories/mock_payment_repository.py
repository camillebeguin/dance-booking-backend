from order.hexagon.gateways.repositories.payment_repository import PaymentRepository
from order.hexagon.models.payment import Payment
from uuid import UUID


class MockPaymentRepository(PaymentRepository):
    def __init__(self):
        self.payments = []

    def feed_with(self, payments: list[Payment]) -> None:
        self.payments = payments

    def save(self, payment: Payment) -> None:
        if payment.id in [p.id for p in self.payments]:
            self.payments[self.payments.index(payment)] = payment
        else:
            self.payments.append(payment)

    def find_by_order_id(self, order_id: UUID) -> Payment | None:
        return next(
            (payment for payment in self.payments if payment.id == order_id), None
        )

    def find_by_payment_intent_id(self, payment_intent_id: str) -> Payment | None:
        return next(
            (
                payment
                for payment in self.payments
                if payment.payment_intent_id == payment_intent_id
            ),
            None,
        )
