from dataclasses import dataclass
from uuid import UUID
from datetime import date


@dataclass
class Credit:
    id: UUID
    expires_at: date | None = None

    def is_expired(self, at_date: date) -> bool:
        """
        Expiry date is exclusive, the credit is expired from the day after the expiry date.
        """
        if self.expires_at is None:
            return False

        return self.expires_at < at_date


@dataclass
class Student:
    id: UUID
    credits: list[Credit]

    def balance(self, at_date: date) -> int:
        return len(
            [credit for credit in self.credits if not credit.is_expired(at_date)]
        )
