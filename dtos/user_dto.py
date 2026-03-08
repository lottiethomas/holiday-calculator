from pydantic import BaseModel

from dtos.holiday_dto import HolidayDto
from dtos.holiday_entitlement_dto import HolidayEntitlementDto
from user import User


class UserDto(BaseModel):
    holiday_entitlement: HolidayEntitlementDto
    holidays: list[HolidayDto] = []

    def to_user(self) -> 'User':
        return User(holiday_entitlement=self.holiday_entitlement.to_holiday_entitlement(),
                    holidays=[holiday_dto.to_holiday() for holiday_dto in self.holidays])
    