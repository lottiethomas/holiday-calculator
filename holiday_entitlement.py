from datetime import datetime
from enum import Enum
from pydantic import BaseModel

import holidays


class HolidayEntitlement(BaseModel):
    """Class for tracking the holiday entitlement of an individual"""

    class CountingMethod(Enum):
        DAYS = 'DAYS'
        HOURS = 'HOURS'

    counting_method: CountingMethod
    amount: float
    working_pattern: tuple[int, int, int, int, int, int, int]
    bank_holidays_counted: bool

    _bank_holidays = holidays.country_holidays('UK', subdiv='ENG')

    def get_cost_of_day(self, day: datetime) -> float:
        if not self.bank_holidays_counted:
            if day in self._bank_holidays:
                return 0
        return self.working_pattern[day.weekday()]
