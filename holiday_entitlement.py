from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class HolidayEntitlement(BaseModel):
    """Class for tracking the holiday entitlement of an individual"""

    class CountingMethod(Enum):
        DAYS = 'DAYS'
        HOURS = 'HOURS'

    counting_method: CountingMethod
    amount: float
    working_pattern: tuple[int, int, int, int, int, int, int]

    def get_cost_of_day(self, day: datetime) -> float:
        return self.working_pattern[day.weekday()]
