from typing import Protocol
from datetime import date


class DateProvider(Protocol):
    def today(self) -> date: ...
