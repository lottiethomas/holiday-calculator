from pydantic import BaseModel

from holiday import Holiday
from holiday_entitlement import HolidayEntitlement


class User(BaseModel):
    holiday_entitlement: HolidayEntitlement
    holidays: list[Holiday]

    def get_cost_for_holiday(self, holiday: Holiday) -> float:
        cost = 0
        for date in holiday.get_dates_in_holiday():
            cost += self.holiday_entitlement.get_cost_of_day(date)
        return cost
