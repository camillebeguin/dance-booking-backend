from order.hexagon.gateways.repositories.order_repository import OrderRepository
from order.hexagon.gateways.repositories.payment_repository import PaymentRepository


class FailPaymentUseCase:
    def __init__(
        self, order_repository: OrderRepository, payment_repository: PaymentRepository
    ):
        self.order_repository = order_repository
        self.payment_repository = payment_repository

    def execute(self, payment_intent_id: str) -> None:
        # TODO: atomic transaction
        payment = self.payment_repository.find_by_payment_intent_id(payment_intent_id)
        order = self.order_repository.get_by_id(payment.id)

        order.fail()
        payment.fail()

        self.order_repository.save(order)
        self.payment_repository.save(payment)
