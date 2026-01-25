from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

import holidays


class HolidayEntitlement(BaseModel):
    """Class for tracking the holiday entitlement of an individual"""
    # TODO validation

    class CountingMethod(Enum):
        DAYS = 'DAYS'
        HOURS = 'HOURS'

    class AmountException(BaseModel):
        start_date: datetime
        end_date: datetime
        amount: float

    counting_method: CountingMethod
    amount: float
    working_pattern: tuple[int, int, int, int, int, int, int]
    bank_holidays_counted: bool
    renewal_date: datetime
    amount_exceptions: Optional[list[AmountException]] = None

    _bank_holidays = holidays.country_holidays('UK', subdiv='ENG')

    def get_cost_of_day(self, day: datetime) -> float:
        if not self.bank_holidays_counted:
            if day in self._bank_holidays:
                return 0
        return self.working_pattern[day.weekday()]

    def get_entitlement_for_date(self, date: datetime) -> float:
        if self.amount_exceptions is None:
            return self.amount
        else:
            # If the date is within an exception range, return the exception amount
            # Otherwise return the entitlement amount
            for exception in self.amount_exceptions:
                if exception.start_date <= date <= exception.end_date:
                    return exception.amount
            return self.amount
