from typing import Protocol
from datetime import datetime


class DateProvider(Protocol):
    def now(self) -> datetime: ...
