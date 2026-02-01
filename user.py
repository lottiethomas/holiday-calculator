from pydantic import BaseModel

from holiday_entitlement import HolidayEntitlement


class User(BaseModel):
    holiday_entitlement: HolidayEntitlement
