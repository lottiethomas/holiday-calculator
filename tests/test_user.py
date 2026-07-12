from datetime import datetime as dt

import pytest

from amount_exception import AmountException
from entitlement_counting_method import EntitlementCountingMethod
from holiday import Holiday
from holiday_entitlement import HolidayEntitlement
from user import User


def mock_daily_cost(mocker, cost=1):
    return mocker.patch("user.HolidayEntitlement.get_cost_of_day", return_value=cost)


@pytest.fixture()
def holiday_entitlement():
    yield HolidayEntitlement(
        counting_method=EntitlementCountingMethod.DAYS,
        amount=273,
        working_pattern=(1, 1, 1, 1, 1, 1, 1),
        bank_holidays_counted=True,
        renewal_month=1,
    )


@pytest.fixture()
def holiday_entitlement_with_exception():
    yield HolidayEntitlement(
        counting_method=EntitlementCountingMethod.DAYS,
        amount=273,
        working_pattern=(1, 1, 1, 1, 1, 1, 1),
        bank_holidays_counted=True,
        renewal_month=1,
        amount_exceptions=[AmountException(dt(2026, 1, 1), dt(2026, 12, 31), 50)],
    )


def test_get_cost_for_holiday(holiday_entitlement, mocker):
    # Given a user with a holiday that is 14 days long
    user = User(holiday_entitlement, [Holiday(dt(2026, 4, 1), dt(2026, 4, 14))])
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the cost of the holiday is retrieved,
    # Then the cost will be 14
    assert user.get_cost_for_holiday(user.holidays[0]) == 14


def test_get_cost_for_single_day_holiday(holiday_entitlement, mocker):
    # Given a user with a one-day holiday
    holiday = Holiday(dt(2026, 4, 1), dt(2026, 4, 1))
    user = User(holiday_entitlement, [holiday])
    # And that the day costs 1
    mock_daily_cost(mocker)
    # When the cost of the holiday is retrieved,
    # Then the cost should include that single day
    assert user.get_cost_for_holiday(holiday) == 1


def test_get_cost_of_holiday_when_user_has_multiple(holiday_entitlement, mocker):
    # Given a user with two holidays, where one is 14 days long and the other is 1 day long
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2026, 4, 15), dt(2026, 4, 15)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the cost of the first holiday is retrieved,
    # Then the cost will be 14
    assert user.get_cost_for_holiday(user.holidays[0]) == 14
    # And when the cost of the second holiday is retrieved,
    # Then the cost will be 1
    assert user.get_cost_for_holiday(user.holidays[1]) == 1


@pytest.mark.parametrize(
    ("holidays", "expected_cost"),
    [
        pytest.param(
            [
                Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
                Holiday(dt(2026, 8, 11), dt(2026, 8, 20)),
            ],
            24,
            id="both_holidays_inside_range",
        ),
        pytest.param(
            [
                Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
                Holiday(dt(2027, 8, 11), dt(2027, 8, 20)),
            ],
            14,
            id="ignores_holiday_outside_range",
        ),
        pytest.param(
            [Holiday(dt(2026, 1, 1), dt(2026, 1, 3))],
            3,
            id="includes_start_boundary",
        ),
        pytest.param(
            [Holiday(dt(2026, 12, 29), dt(2026, 12, 31))],
            3,
            id="includes_end_boundary",
        ),
        pytest.param(
            [Holiday(dt(2027, 1, 1), dt(2027, 1, 10))],
            0,
            id="returns_zero_when_none_match",
        ),
    ],
)
def test_get_cost_of_all_holidays_in_date_range(
    holiday_entitlement, mocker, holidays, expected_cost
):
    user = User(holiday_entitlement, holidays)
    mock_daily_cost(mocker)
    assert (
        user.get_cost_for_holidays_in_date_range(
            start_date=dt(2026, 1, 1), end_date=dt(2026, 12, 31)
        )
        == expected_cost
    )


def test_get_cost_of_all_holidays_in_year(holiday_entitlement, mocker):
    # Given a user with two holidays where both fall within the holiday year
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2026, 8, 11), dt(2026, 8, 20)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the cost of holiday for 2026 is requested,
    # Then the cost will be the sum of the two holidays
    assert user.get_cost_for_holidays_in_holiday_year_starting_in(2026) == 24


def test_get_cost_of_all_holidays_in_year_ignores_out_of_range(
    holiday_entitlement, mocker
):
    # Given a user with two holidays, where one falls outside the target entitlement year
    holiday_entitlement.renewal_month = 4
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2027, 8, 11), dt(2027, 8, 20)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the cost of holidays in year starting in 2026 is requested
    # Then the cost will be only the holiday that falls in the range
    assert user.get_cost_for_holidays_in_holiday_year_starting_in(2026) == 14


def test_get_cost_for_holidays_in_holiday_year_with_april_renewal_includes_full_year_range(
    holiday_entitlement, mocker
):
    # Given an entitlement year that starts in April
    holiday_entitlement.renewal_month = 4
    # And a user with holidays spanning across renewal boundaries
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 1)),
            Holiday(dt(2027, 3, 31), dt(2027, 3, 31)),
            Holiday(dt(2027, 4, 1), dt(2027, 4, 1)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the cost of holidays in the holiday year starting in 2026 is requested,
    # Then dates from 2026-04-01 through 2027-03-31 should be included
    assert user.get_cost_for_holidays_in_holiday_year_starting_in(2026) == 2


@pytest.mark.parametrize(
    ("year", "expected_cost"),
    [
        pytest.param(2026, 3, id="counts_only_part_before_renewal_boundary"),
        pytest.param(2027, 2, id="counts_only_part_after_renewal_boundary"),
    ],
)
def test_get_cost_for_holidays_in_holiday_year_counts_only_matching_part_of_spanning_holiday(
    holiday_entitlement,
    mocker,
    year,
    expected_cost,
):
    holiday_entitlement.renewal_month = 4
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2027, 3, 29), dt(2027, 4, 2)),
        ],
    )
    mock_daily_cost(mocker)
    assert user.get_cost_for_holidays_in_holiday_year_starting_in(year) == expected_cost


def test_remaining_allowance_for_year(holiday_entitlement, mocker):
    # Given a user with two holidays where both fall within the holiday year
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2026, 8, 11), dt(2026, 8, 20)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the remaining entitlement for 2026 is requested,
    # Then the answer will be the total allowance less the cost of both holidays
    assert (
        user.get_remaining_allowance_for_year_starting_in(2026)
        == holiday_entitlement.amount - 24
    )


def test_remaining_allowance_for_year_ignores_out_of_range(holiday_entitlement, mocker):
    # Given a user with two holidays, where one falls outside the target entitlement year
    holiday_entitlement.renewal_month = 4
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2027, 8, 11), dt(2027, 8, 20)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the remaining entitlement for 2026 is requested,
    # Then the answer will be the total allowance less only the cost of the holiday in the year
    assert (
        user.get_remaining_allowance_for_year_starting_in(2026)
        == holiday_entitlement.amount - 14
    )


def test_remaining_allowance_for_year_uses_amount_exception(
    holiday_entitlement_with_exception, mocker
):
    # Given a user with two holidays where both fall within the holiday year
    user = User(
        holiday_entitlement_with_exception,
        [
            Holiday(dt(2026, 4, 1), dt(2026, 4, 14)),
            Holiday(dt(2026, 8, 11), dt(2026, 8, 20)),
        ],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the remaining entitlement for 2026 is requested,
    # Then the answer will be the total allowance for that year less the cost of both holidays
    assert (
        user.get_remaining_allowance_for_year_starting_in(2026)
        == holiday_entitlement_with_exception.amount_exceptions[0].amount - 24
    )


def test_remaining_allowance_for_year_with_no_holidays_returns_full_entitlement(
    holiday_entitlement,
):
    # Given a user with no holidays
    user = User(holiday_entitlement, [])
    # When the remaining allowance is requested,
    # Then the full entitlement should remain
    assert (
        user.get_remaining_allowance_for_year_starting_in(2026)
        == holiday_entitlement.amount
    )


def test_remaining_allowance_for_year_uses_default_amount_when_exception_does_not_apply(
    holiday_entitlement_with_exception, mocker
):
    # Given an amount exception that only applies in 2026
    user = User(
        holiday_entitlement_with_exception,
        [Holiday(dt(2027, 4, 1), dt(2027, 4, 2))],
    )
    # And that each day costs 1
    mock_daily_cost(mocker)
    # When the remaining entitlement for a year outside the exception is requested,
    # Then the default entitlement amount should be used
    assert (
        user.get_remaining_allowance_for_year_starting_in(2027)
        == holiday_entitlement_with_exception.amount - 2
    )


@pytest.mark.parametrize(
    ("year", "deducted_cost"),
    [
        pytest.param(2026, 3, id="deducts_only_part_before_renewal_boundary"),
        pytest.param(2027, 2, id="deducts_only_part_after_renewal_boundary"),
    ],
)
def test_remaining_allowance_for_year_deducts_only_matching_part_of_spanning_holiday(
    holiday_entitlement,
    mocker,
    year,
    deducted_cost,
):
    holiday_entitlement.renewal_month = 4
    user = User(
        holiday_entitlement,
        [
            Holiday(dt(2027, 3, 29), dt(2027, 4, 2)),
        ],
    )
    mock_daily_cost(mocker)
    assert (
        user.get_remaining_allowance_for_year_starting_in(year)
        == holiday_entitlement.amount - deducted_cost
    )
