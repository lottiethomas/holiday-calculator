from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable


@dataclass
class Holiday:
    start_date: date
    end_date: date
    description: str = ""

    def __post_init__(self) -> None:
        if self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date")

    def get_dates_in_holiday(
        self, from_date: date | None = None, to_date: date | None = None
    ) -> Iterable[date]:
        start_date = max(self.start_date, from_date) if from_date else self.start_date
        end_date = min(self.end_date, to_date) if to_date else self.end_date

        return [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ]

    def is_in_date_range(self, from_date: date, to_date: date) -> bool:
        """Returns true if any day of the holiday is within the date range"""
        return self.start_date <= to_date and from_date <= self.end_date
