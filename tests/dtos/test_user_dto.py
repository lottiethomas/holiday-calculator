import pytest
from pydantic import ValidationError

from dtos.holiday_dto import HolidayDto
from dtos.holiday_entitlement_dto import HolidayEntitlementDto
from dtos.user_dto import UserDto


def test_user_must_have_entitlement():
    # Given a user without a holiday entitlement
    # When the user is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        UserDto.model_validate({})


def test_user_may_not_have_holidays():
    # Given a holiday entitlement
    entitlement = HolidayEntitlementDto.model_validate(
        {'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1, 1, 1, 1, 1, 1, 1],
         'bank_holidays_counted': True, 'renewal_month': 1})
    # When a user is created without any holidays,
    # No validation exception should be thrown
    UserDto.model_validate({'holiday_entitlement': entitlement})


def test_dto_can_be_converted_to_user():
    # Given a holiday entitlement
    entitlement = HolidayEntitlementDto.model_validate(
        {'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1, 1, 1, 1, 1, 1, 1],
         'bank_holidays_counted': True, 'renewal_month': 1})
    # And a list of holidays
    holiday = HolidayDto.model_validate({'start_date': '2026-01-01', 'end_date': '2026-01-01'})
    holidays = [holiday]
    # When the DTO is converted to a user,
    user = UserDto.model_validate({'holiday_entitlement': entitlement, 'holidays': holidays}).to_user()
    # Then the holidays should be converted to a list of Holiday objects
    assert isinstance(user.holidays, list)
    assert user.holidays[0] == holiday.to_holiday()
    # And the user should have the correct entitlement
    assert user.holiday_entitlement == entitlement.to_holiday_entitlement()
