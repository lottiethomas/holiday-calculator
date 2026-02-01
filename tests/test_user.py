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
    mocker.patch('user.HolidayEntitlement.get_cost_of_day', return_value=1)
    assert user.get_cost_for_holiday(user.holidays[0]) == 14
