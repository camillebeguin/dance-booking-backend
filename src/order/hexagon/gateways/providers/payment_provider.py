from typing import Protocol


class PaymentProvider(Protocol):
    def create_payment_intent(self, idempotency_key: str) -> str: ...
