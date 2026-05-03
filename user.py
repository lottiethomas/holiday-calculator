from dataclasses import dataclass
from datetime import datetime, timedelta

from holiday import Holiday
from holiday_entitlement import HolidayEntitlement


@dataclass
class User:
    holiday_entitlement: HolidayEntitlement
    holidays: list[Holiday]

    def get_cost_for_holiday(self, holiday: Holiday) -> float:
        cost = 0
        for date in holiday.get_dates_in_holiday():
            cost += self.holiday_entitlement.get_cost_of_day(date)
        return cost

    def get_cost_for_holidays_in_date_range(self, start_date: datetime, end_date: datetime) -> float:
        cost = 0
        for holiday in self.holidays:
            if start_date <= holiday.start_date <= end_date:
                print(f"Holiday {holiday.description} costs {self.get_cost_for_holiday(holiday)}")
                cost += self.get_cost_for_holiday(holiday)
        return cost

    def get_cost_for_holidays_in_holiday_year_starting_in(self, year: int) -> float:
        start_date = datetime(year, self.holiday_entitlement.renewal_month, 1)
        end_date = datetime(year + 1, self.holiday_entitlement.renewal_month, 1) - timedelta(days=1)
        return self.get_cost_for_holidays_in_date_range(start_date, end_date)

    def get_remaining_allowance_for_year_starting_in(self, year: int) -> float:
        return self.holiday_entitlement.get_entitlement_for_date(datetime(year, self.holiday_entitlement.renewal_month, 1)) - self.get_cost_for_holidays_in_holiday_year_starting_in(year)
