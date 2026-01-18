from datetime import datetime, timezone
import pytest

from holiday_entitlement import HolidayEntitlement


@pytest.fixture()
def hours_entitlement() -> HolidayEntitlement:
    return HolidayEntitlement.model_validate({'counting_method': 'HOURS', 'amount': 273, 'working_pattern': [8,5,0,3,4,0,7]})


@pytest.fixture()
def days_entitlement() -> HolidayEntitlement:
    return HolidayEntitlement.model_validate({'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1,0,0,1,0,1,1]})


@pytest.mark.parametrize("date,expected_cost",
                         [(datetime(2026, 1, 19), 8),
                          (datetime(2026, 1, 20), 5),
                          (datetime(2026, 1, 21), 0),
                          (datetime(2026, 1, 22), 3),
                          (datetime(2026, 1, 23), 4),
                          (datetime(2026, 1, 24), 0),
                          (datetime(2026, 1, 25), 7)])
def test_cost_of_day_calculated_in_hours(hours_entitlement, date, expected_cost):
    cost = hours_entitlement.get_cost_of_day(date)
    assert cost == expected_cost


@pytest.mark.parametrize("date,expected_cost",
                         [(datetime(2026, 1, 19), 1),
                          (datetime(2026, 1, 20), 0),
                          (datetime(2026, 1, 21), 0),
                          (datetime(2026, 1, 22), 1),
                          (datetime(2026, 1, 23), 0),
                          (datetime(2026, 1, 24), 1),
                          (datetime(2026, 1, 25), 1)])
def test_cost_of_day_calculated_in_days(days_entitlement, date, expected_cost):
    cost = days_entitlement.get_cost_of_day(date)
    assert cost == expected_cost
