from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

import holidays

from amount_exception import AmountException
from entitlement_counting_method import EntitlementCountingMethod


@dataclass
class HolidayEntitlement:
    """Class for tracking the holiday entitlement of an individual"""
    counting_method: EntitlementCountingMethod
    amount: float
    working_pattern: Tuple[float, float, float, float, float, float, float]
    bank_holidays_counted: bool
    renewal_month: int
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
