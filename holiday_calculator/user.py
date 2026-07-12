from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Iterable

from holiday import Holiday
from holiday_entitlement import HolidayEntitlement


@dataclass
class User:
    holiday_entitlement: HolidayEntitlement
    holidays: list[Holiday] = field(default_factory=list)

    def _get_cost_for_dates(self, dates: Iterable[date]) -> float:
        return sum(self.holiday_entitlement.get_cost_of_day(a_date) for a_date in dates)

    def get_cost_for_holiday(self, holiday: Holiday) -> float:
        return self._get_cost_for_dates(dates=holiday.get_dates_in_holiday())

    def get_cost_for_holidays_in_date_range(
        self, start_date: date, end_date: date
    ) -> float:
        dates_to_count = []
        for holiday in self.holidays:
            if holiday.is_in_date_range(start_date, end_date):
                dates_to_count.extend(
                    holiday.get_dates_in_holiday(start_date, end_date)
                )
        dates_to_count = set(dates_to_count)
        return self._get_cost_for_dates(dates_to_count)

    def _get_holiday_year_date_range(self, year: int) -> tuple[date, date]:
        start_date = date(year, self.holiday_entitlement.renewal_month, 1)
        end_date = date(
            year + 1, self.holiday_entitlement.renewal_month, 1
        ) - timedelta(days=1)
        return start_date, end_date

    def get_cost_for_holidays_in_holiday_year_starting_in(self, year: int) -> float:
        start_date, end_date = self._get_holiday_year_date_range(year)
        return self.get_cost_for_holidays_in_date_range(start_date, end_date)

    def get_remaining_allowance_for_year_starting_in(self, year: int) -> float:
        year_date, _ = self._get_holiday_year_date_range(year)
        return self.holiday_entitlement.get_entitlement_on_date(
            year_date
        ) - self.get_cost_for_holidays_in_holiday_year_starting_in(year)
