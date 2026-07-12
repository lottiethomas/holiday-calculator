from dataclasses import dataclass
from datetime import date


@dataclass
class AmountException:
    start_date: date
    end_date: date
    amount: float

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self
