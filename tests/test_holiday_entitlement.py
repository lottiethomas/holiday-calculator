from datetime import date

import pytest

from amount_exception import AmountException
from entitlement_counting_method import EntitlementCountingMethod
from holiday_entitlement import HolidayEntitlement


@pytest.fixture()
def hours_entitlement():
    yield HolidayEntitlement(
        counting_method=EntitlementCountingMethod.HOURS,
        amount=273,
        working_pattern=(8, 5, 0, 3, 4.5, 0, 7),
        bank_holidays_counted=True,
        renewal_month=1,
    )


@pytest.fixture()
def days_entitlement():
    yield HolidayEntitlement(
        counting_method=EntitlementCountingMethod.DAYS,
        amount=273,
        working_pattern=(1, 0, 0, 1, 0, 1, 1),
        bank_holidays_counted=False,
        renewal_month=1,
    )


@pytest.fixture()
def days_entitlement_with_amount_exceptions():
    yield HolidayEntitlement(
        counting_method=EntitlementCountingMethod.DAYS,
        amount=273,
        working_pattern=(1, 0, 0, 1, 0, 1, 1),
        bank_holidays_counted=False,
        renewal_month=4,
        amount_exceptions=[
            AmountException(
                start_date=date(2025, 4, 1),
                end_date=date(2026, 3, 31),
                amount=50,
            ),
            AmountException(
                start_date=date(2027, 4, 1),
                end_date=date(2028, 3, 31),
                amount=94,
            ),
        ],
    )


@pytest.mark.parametrize(
    "day,expected_cost",
    [
        (date(2026, 1, 19), 8),
        (date(2026, 1, 20), 5),
        (date(2026, 1, 21), 0),
        (date(2026, 1, 22), 3),
        (date(2026, 1, 23), 4.5),
        (date(2026, 1, 24), 0),
        (date(2026, 1, 25), 7),
    ],
)
def test_cost_of_day_calculated_in_hours(hours_entitlement, day, expected_cost):
    cost = hours_entitlement.get_cost_of_day(day)
    assert cost == expected_cost


@pytest.mark.parametrize(
    "day,expected_cost",
    [
        (date(2026, 1, 19), 1),
        (date(2026, 1, 20), 0),
        (date(2026, 1, 21), 0),
        (date(2026, 1, 22), 1),
        (date(2026, 1, 23), 0),
        (date(2026, 1, 24), 1),
        (date(2026, 1, 25), 1),
    ],
)
def test_cost_of_day_calculated_in_days(days_entitlement, day, expected_cost):
    cost = days_entitlement.get_cost_of_day(day)
    assert cost == expected_cost


def test_bank_holiday_free_when_not_counted(days_entitlement):
    cost = days_entitlement.get_cost_of_day(date(2026, 1, 1))  # Bank holiday Thursday
    assert cost == 0


def test_bank_holiday_costs_when_counted(hours_entitlement):
    cost = hours_entitlement.get_cost_of_day(date(2026, 1, 1))  # Bank holiday Thursday
    assert cost == 3


def test_get_entitlement_for_date(days_entitlement):
    assert days_entitlement.get_entitlement_on_date(date(2026, 1, 1)) == 273


@pytest.mark.parametrize(
    "on_date,expected",
    [
        (date(2025, 4, 1), 50),
        (date(2026, 4, 1), 273),
        (date(2027, 4, 1), 94),
        (date(2025, 3, 31), 273),
        (date(2026, 5, 1), 273),
        (date(2028, 4, 1), 273),
    ],
)
def test_amount_exception_applied(
    days_entitlement_with_amount_exceptions, on_date, expected
):
    assert (
        days_entitlement_with_amount_exceptions.get_entitlement_on_date(on_date)
        == expected
    )


@pytest.mark.parametrize(
    "renewal_month,starting_year,expected_string",
    [
        (1, 2026, "2026"),
        (1, 2027, "2027"),
        (4, 2026, "April 2026 to March 2027"),
        (9, 2027, "September 2027 to August 2028"),
    ],
)
def test_get_description_for_year_returns_expected_string(
    days_entitlement, renewal_month, starting_year, expected_string
):
    # Given an entitlement that starts on the given renewal month
    days_entitlement.renewal_month = renewal_month
    # When the description of the year is requested
    description = days_entitlement.get_description_of_entitlement_for_year_starting_in(
        starting_year
    )
    # Then the description should be the expected string
    assert description == expected_string
