from dataclasses import dataclass
from enum import StrEnum


class SupportedCurrency(StrEnum):
    EUR = "EUR"


@dataclass
class Money:
    amount: int
    currency: SupportedCurrency

    def __add__(self, other: "Money") -> "Money":
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )
