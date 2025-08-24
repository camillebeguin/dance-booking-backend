from order.hexagon.gateways.repositories.payment_repository import PaymentRepository
from order.hexagon.gateways.providers.payment_provider import PaymentProvider

from order.hexagon.models.payment import Payment
from order.hexagon.models.exceptions import PaymentAlreadyInitiatedException


class InitiatePaymentUseCase:
    def __init__(
        self, payment_repository: PaymentRepository, payment_provider: PaymentProvider
    ):
        self.payment_repository = payment_repository
        self.payment_provider = payment_provider

    def execute(self, order_id: str) -> None:
        if self.payment_repository.find_by_order_id(order_id):
            raise PaymentAlreadyInitiatedException

        # generate idempotent payment intent
        payment_intent_id = self.payment_provider.create_payment_intent(
            idempotency_key=order_id,
        )

        payment = Payment.create(order_id=order_id, payment_intent_id=payment_intent_id)
        self.payment_repository.save(payment)
