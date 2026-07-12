from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Holiday:
    start_date: datetime
    end_date: datetime
    description: str = ""

    def get_dates_in_holiday(
        self, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[datetime]:
        start_date = (
            self.start_date
            if from_date is None or from_date < self.start_date
            else from_date
        )
        end_date = (
            self.end_date if to_date is None or to_date > self.end_date else to_date
        )
        return [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ]

    def is_in_date_range(self, from_date: datetime, to_date: datetime) -> bool:
        """Returns true if any day of the holiday is within the date range"""
        return self.start_date <= to_date and from_date <= self.end_date
