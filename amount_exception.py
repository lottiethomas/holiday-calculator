from dataclasses import dataclass
from datetime import date


@dataclass
class AmountException:
    start_date: date
    end_date: date
    amount: float
