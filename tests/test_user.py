from datetime import datetime

import pytest

from entitlement_counting_method import EntitlementCountingMethod
from holiday import Holiday
from holiday_entitlement import HolidayEntitlement
from user import User


@pytest.fixture()
def holiday():
    yield Holiday(start_date=datetime(2026, 1, 1), end_date=datetime(2026, 1, 14))


@pytest.fixture()
def holiday_entitlement():
    yield HolidayEntitlement(counting_method=EntitlementCountingMethod.DAYS, amount=273,
                             working_pattern=(1, 1, 1, 1, 1, 1, 1), bank_holidays_counted=True, renewal_month=1)


@pytest.fixture()
def user(holiday, holiday_entitlement):
    yield User(holiday_entitlement=holiday_entitlement, holidays=[holiday])


def test_get_cost_for_holiday(user, mocker):
    # Given a user with a holiday that is 14 days long
    # And that each day costs 1
    mocker.patch('user.HolidayEntitlement.get_cost_of_day', return_value=1)
    # When the cost of the holiday is retrieved
    # Then the cost will be 14
    assert user.get_cost_for_holiday(user.holidays[0]) == 14


def test_get_cost_of_all_holidays_in_date_range(holiday_entitlement, mocker):
    # Given a user with two holidays where both fall within the date range
    user = User(holiday_entitlement=holiday_entitlement,
                holidays=[
                    Holiday(start_date=datetime(2026, 4, 1), end_date=datetime(2026, 4, 14)),
                    Holiday(start_date=datetime(2026, 8, 11), end_date=datetime(2026, 8, 20))
                ])
    # And that each day costs 1
    mocker.patch('user.HolidayEntitlement.get_cost_of_day', return_value=1)
    # When the cost of holiday between 2026/01/01 and 2026/12/31 is retrieved
    # Then the cost will be the sum of the two holidays
    assert user.get_cost_for_holidays_in_date_range(start_date=datetime(2026, 1, 1),
                                                    end_date=datetime(2026, 12, 31)) == 24


def test_get_cost_of_all_holidays_in_range_ignores_out_of_range(holiday_entitlement, mocker):
    # Given a user with two holidays where one falls outside the date range
    user = User(holiday_entitlement=holiday_entitlement,
                holidays=[
                    Holiday(start_date=datetime(2026, 4, 1), end_date=datetime(2026, 4, 14)),
                    Holiday(start_date=datetime(2027, 8, 11), end_date=datetime(2027, 8, 20))
                ])
    # And that each day costs 1
    mocker.patch('user.HolidayEntitlement.get_cost_of_day', return_value=1)
    # When the cost of holiday between 2026/01/01 and 2026/12/31 is retrieved
    # Then the cost will be only the holiday that falls in the range
    assert user.get_cost_for_holidays_in_date_range(start_date=datetime(2026, 1, 1),
                                                    end_date=datetime(2026, 12, 31)) == 14
