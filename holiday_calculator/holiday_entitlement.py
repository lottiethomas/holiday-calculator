import calendar
from dataclasses import dataclass
from datetime import date
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

    _bank_holidays = holidays.country_holidays("UK", subdiv="ENG")

    def __post_init__(self):
        if len(self.working_pattern) != 7:
            raise ValueError("Working pattern must be 7 days long")
        if not 1 <= self.renewal_month <= 12:
            raise ValueError("Renewal month must be between 1 and 12")
        if self.counting_method is EntitlementCountingMethod.DAYS:
            if self.amount > 366:
                raise ValueError("Amount must not exceed a year")
            for day in self.working_pattern:
                if not 0 <= day <= 1:
                    raise ValueError(
                        "When the counting method is DAYS, each day must be between 0 and 1"
                    )
        if self.counting_method is EntitlementCountingMethod.HOURS:
            if self.amount > 8784:
                raise ValueError("Amount must not exceed a year")
            for day in self.working_pattern:
                if not 0 <= day <= 24:
                    raise ValueError(
                        "When the counting method is HOURS, each day must be between 0 and 24"
                    )
        return self

    def get_description_of_entitlement_for_year_starting_in(self, year: int) -> str:
        if self.renewal_month == 1:
            return str(year)
        else:
            return (
                f"{calendar.month_name[self.renewal_month]} {str(year)} to "
                f"{calendar.month_name[self.renewal_month - 1]} {str(year + 1)}"
            )

    def get_cost_of_day(self, day: date) -> float:
        if not self.bank_holidays_counted:
            if day in self._bank_holidays:
                return 0
        return self.working_pattern[day.weekday()]

    def get_entitlement_on_date(self, on_date: date) -> float:
        if self.amount_exceptions is None:
            return self.amount
        else:
            # If the date is within an exception range, return the exception amount
            # Otherwise return the entitlement amount
            for exception in self.amount_exceptions:
                if exception.start_date <= on_date <= exception.end_date:
                    return exception.amount
            return self.amount
