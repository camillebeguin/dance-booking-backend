from booking.hexagon.gateways.providers.date_provider import DateProvider
from datetime import datetime


class DeterministicDateProvider(DateProvider):
    def __init__(self, current_date: datetime):
        self.current_date = current_date

    def now(self) -> datetime:
        return self.current_date
