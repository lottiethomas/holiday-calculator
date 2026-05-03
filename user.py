from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable

from holiday import Holiday
from holiday_entitlement import HolidayEntitlement


@dataclass
class User:
    holiday_entitlement: HolidayEntitlement
    holidays: list[Holiday] = field(default_factory=list)

    def _get_cost_for_dates(self, dates: Iterable[datetime]) -> float:
        return sum(self.holiday_entitlement.get_cost_of_day(date) for date in dates)

    def get_cost_for_holiday(self, holiday: Holiday) -> float:
        return self._get_cost_for_dates(dates=holiday.get_dates_in_holiday())

    def get_cost_for_holidays_in_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> float:
        return sum(
            self._get_cost_for_dates(holiday.get_dates_in_holiday(start_date, end_date))
            for holiday in self.holidays
            if holiday.is_in_date_range(start_date, end_date)
        )

    def _get_holiday_year_date_range(self, year: int) -> tuple[datetime, datetime]:
        start_date = datetime(year, self.holiday_entitlement.renewal_month, 1)
        end_date = datetime(
            year + 1, self.holiday_entitlement.renewal_month, 1
        ) - timedelta(days=1)
        return start_date, end_date

    def get_cost_for_holidays_in_holiday_year_starting_in(self, year: int) -> float:
        start_date, end_date = self._get_holiday_year_date_range(year)
        return self.get_cost_for_holidays_in_date_range(start_date, end_date)

    def get_remaining_allowance_for_year_starting_in(self, year: int) -> float:
        year_date, _ = self._get_holiday_year_date_range(year)
        return self.holiday_entitlement.get_entitlement_for_date(
            year_date
        ) - self.get_cost_for_holidays_in_holiday_year_starting_in(year)
