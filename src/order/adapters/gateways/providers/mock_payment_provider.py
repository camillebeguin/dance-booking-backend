from order.hexagon.gateways.providers.payment_provider import PaymentProvider


class MockPaymentProvider(PaymentProvider):
    def __init__(self, keys_to_payment_intents: dict[str, str]):
        self.keys_to_payment_intents = keys_to_payment_intents

    def create_payment_intent(self, idempotency_key: str) -> str:
        return self.keys_to_payment_intents.get(idempotency_key)
