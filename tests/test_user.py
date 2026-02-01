import pytest

from holiday import Holiday
from holiday_entitlement import HolidayEntitlement
from user import User


@pytest.fixture()
def holiday():
    yield Holiday.model_validate({'start_date': '2026-01-01', 'end_date': '2026-01-14'})


@pytest.fixture()
def holiday_entitlement():
    yield HolidayEntitlement.model_validate(
        {'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1, 1, 1, 1, 1, 1, 1],
         'bank_holidays_counted': True, 'renewal_date': '2026-01-01'})


@pytest.fixture()
def user(holiday, holiday_entitlement):
    yield User.model_validate({'holiday_entitlement': holiday_entitlement, 'holidays': [holiday]})


def test_get_cost_for_holiday(user, mocker):
    mocker.patch('user.HolidayEntitlement.get_cost_of_day', return_value=1)
    assert user.get_cost_for_holiday(user.holidays[0]) == 14
