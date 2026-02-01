from datetime import datetime
import pytest

from holiday_entitlement import HolidayEntitlement


@pytest.fixture()
def hours_entitlement():
    yield HolidayEntitlement.model_validate(
        {'counting_method': 'HOURS', 'amount': 273, 'working_pattern': [8, 5, 0, 3, 4, 0, 7],
         'bank_holidays_counted': True, "renewal_date": "2026-01-01"})


@pytest.fixture()
def days_entitlement():
    yield HolidayEntitlement.model_validate(
        {'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1, 0, 0, 1, 0, 1, 1],
         'bank_holidays_counted': False, "renewal_date": "2026-01-01"})


@pytest.fixture()
def days_entitlement_with_amount_exceptions():
    yield HolidayEntitlement.model_validate(
        {'counting_method': 'DAYS', 'amount': 273, 'working_pattern': [1, 0, 0, 1, 0, 1, 1],
         'bank_holidays_counted': False, "renewal_date": "2026-04-01",
         'amount_exceptions': [{'start_date': '2025-04-01', 'end_date': '2026-03-31', 'amount': 50},
                               {'start_date': '2027-04-01', 'end_date': '2028-03-31', 'amount': 94}]}
    )


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


def test_bank_holiday_free_when_not_counted(days_entitlement):
    cost = days_entitlement.get_cost_of_day(datetime(2026, 1, 1))  # Bank holiday Thursday
    assert cost == 0


def test_bank_holiday_costs_when_counted(hours_entitlement):
    cost = hours_entitlement.get_cost_of_day(datetime(2026, 1, 1))  # Bank holiday Thursday
    assert cost == 3


def test_get_entitlement_for_date(days_entitlement):
    assert days_entitlement.get_entitlement_for_date(datetime(2026, 1, 1)) == 273


@pytest.mark.parametrize("date,expected", [('2025-04-01', 50), ('2026-04-01', 273), ('2027-04-01', 94),
                                           ('2025-03-31', 273), ('2026-05-01', 273), ('2028-04-01', 273)])
def test_amount_exception_applied(days_entitlement_with_amount_exceptions, date, expected):
    on_date = datetime.strptime(date, '%Y-%m-%d')
    assert days_entitlement_with_amount_exceptions.get_entitlement_for_date(on_date) == expected
