from order.hexagon.gateways.repositories.order_repository import OrderRepository
from order.hexagon.gateways.repositories.payment_repository import PaymentRepository
from order.hexagon.gateways.providers.payment_provider import PaymentProvider
from order.hexagon.models.payment import Payment


class ConfirmOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_provider: PaymentProvider,
        payment_repository: PaymentRepository,
    ):
        self.order_repository = order_repository
        self.payment_provider = payment_provider
        self.payment_repository = payment_repository

    def execute(self, order_id: str):
        order = self.order_repository.get_by_id(order_id)

        # generate a payment intent idempotently
        payment_intent = self.payment_provider.create_payment_intent(
            idempotency_key=order_id,
        )
        payment = Payment.create(
            order_id=order_id,
            payment_intent_id=payment_intent,
            amount=order.total_amount,
        )

        # confirm order
        order.confirm()

        self.order_repository.save(order)
        self.payment_repository.save(payment)
