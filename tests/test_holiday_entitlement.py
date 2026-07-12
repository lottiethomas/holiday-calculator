from datetime import date

import pytest

from amount_exception import AmountException
from entitlement_counting_method import EntitlementCountingMethod
from holiday_entitlement import HolidayEntitlement


def make_entitlement(
    counting_method: EntitlementCountingMethod = EntitlementCountingMethod.DAYS,
    amount: float = 273,
    working_pattern: tuple[float, float, float, float, float, float, float] = (
        1,
        0,
        0,
        1,
        0,
        1,
        1,
    ),
    bank_holidays_counted: bool = True,
    renewal_month: int = 1,
    amount_exceptions: list[AmountException] = None,
):
    return HolidayEntitlement(
        counting_method=counting_method,
        amount=amount,
        working_pattern=working_pattern,
        bank_holidays_counted=bank_holidays_counted,
        renewal_month=renewal_month,
        amount_exceptions=amount_exceptions,
    )


@pytest.mark.parametrize(
    "counting_method, amount",
    [
        (EntitlementCountingMethod.DAYS, 365),
        (EntitlementCountingMethod.HOURS, 8760),  # number of hours in a year
        (EntitlementCountingMethod.DAYS, 366),
        (EntitlementCountingMethod.HOURS, 8784),  # number of hours in a leap year
    ],
)
def test_amount_can_be_a_year(counting_method, amount):
    # Given a holiday entitlement where the amount is equal to a year
    # When the holiday entitlement is created,
    # No validation exception should be thrown
    make_entitlement(counting_method, amount)


@pytest.mark.parametrize(
    "counting_method, amount",
    [
        (EntitlementCountingMethod.DAYS, 367),
        (EntitlementCountingMethod.HOURS, 8785),  # hours in a leap year + 1
    ],
)
def test_amount_cannot_be_more_than_a_year(counting_method, amount):
    # Given a holiday entitlement where the amount is equal to a year
    # When the holiday entitlement is created,
    # No validation exception should be thrown
    with pytest.raises(ValueError):
        make_entitlement(counting_method, amount)


# fmt: off
@pytest.mark.parametrize(
    "working_pattern",
    [
        (1.0,),
        (1.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
    ],
)
def test_working_pattern_must_have_length_seven(working_pattern):
    # Given a holiday entitlement with a working pattern that is not of length 7
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValueError):
        make_entitlement(working_pattern=working_pattern)


@pytest.mark.parametrize("counting_method, working_pattern",
                         [
                             (EntitlementCountingMethod.DAYS, (1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.1, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.1, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, 1.1, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, 1.0, 1.1, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.1,)),
                             (EntitlementCountingMethod.HOURS, (24.1, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.1, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.1, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.1, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, 24.1, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, 24.0, 24.1, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.1,)),
                         ])
def test_working_pattern_entry_must_not_exceed_1_day(counting_method, working_pattern):
    # Given a holiday entitlement with a working pattern where an entry is greater than 1 day
    # When the holiday entitlement is created,
    # A value error should be thrown
    with pytest.raises(ValueError):
        make_entitlement(counting_method=counting_method, working_pattern=working_pattern)


@pytest.mark.parametrize("counting_method, working_pattern",
                         [
                             (EntitlementCountingMethod.DAYS, (-1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, -1, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, -1, 1.0, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, -1, 1.0, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, -1, 1.0, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, 1.0, -1, 1.0,)),
                             (EntitlementCountingMethod.DAYS, (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1,)),
                             (EntitlementCountingMethod.HOURS, (-1, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, -1, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, -1, 24.0, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, -1, 24.0, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, -1, 24.0, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, 24.0, -1, 24.0,)),
                             (EntitlementCountingMethod.HOURS, (24.0, 24.0, 24.0, 24.0, 24.0, 24.0, -1,)),
                         ])
def test_working_pattern_entry_must_not_be_negative(counting_method, working_pattern):
    # Given a holiday entitlement with a working pattern where an entry is negative
    # When the holiday entitlement is created,
    # A value error should be thrown
    with pytest.raises(ValueError):
        make_entitlement(counting_method=counting_method, working_pattern=working_pattern)


@pytest.mark.parametrize(
    "renewal_month",
    [
        0,
        13,
    ],
)
def test_renewal_month_must_be_one_to_twelve(renewal_month):
    # Given a holiday entitlement where the renewal month is not between 1 and 12
    # When the holiday entitlement is created,
    # A value error should be thrown
    with pytest.raises(ValueError):
        make_entitlement(renewal_month=renewal_month)


@pytest.mark.parametrize(
    "renewal_month",
    [
        1,
        6,
        12,
    ],
)
def test_renewal_month_may_be_between_one_and_twelve(renewal_month):
    # Given a holiday entitlement where the renewal month is between 1 and 12
    # When the holiday entitlement is created,
    # No error should be thrown
    make_entitlement(renewal_month=renewal_month)


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
def test_cost_of_day_calculated_in_hours(day, expected_cost):
    # Given an entitlement counted in hours with different hours each day
    entitlement = make_entitlement(
        counting_method=EntitlementCountingMethod.HOURS,
        working_pattern=(8, 5, 0, 3, 4.5, 0, 7),
    )
    # When the cost of a day is requested
    cost = entitlement.get_cost_of_day(day)
    # The cost should be the expected number of hours
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
def test_cost_of_day_calculated_in_days(day, expected_cost):
    # Given an entitlement counted in days
    entitlement = make_entitlement()
    # When the cost of a day is requested
    cost = entitlement.get_cost_of_day(day)
    # Then the cost is whether that day is worked
    assert cost == expected_cost


def test_bank_holiday_free_when_not_counted():
    # Given an entitlement where bank holidays are not counted
    entitlement = make_entitlement(bank_holidays_counted=False)
    # When the cost of a bank holiday is requested
    cost = entitlement.get_cost_of_day(date(2026, 1, 1))  # Bank holiday Thursday
    # Then the cost should be zero
    assert cost == 0


def test_bank_holiday_costs_when_counted():
    # Given an entitlement where bank holidays are counted and Thursdays are working days
    entitlement = make_entitlement(
        working_pattern=(1, 0, 0, 1, 0, 1, 1), bank_holidays_counted=True
    )
    # When the cost of a bank holiday is requested
    cost = entitlement.get_cost_of_day(date(2026, 1, 1))  # Bank holiday Thursday
    # Then the cost should 1 because the day is a working day
    assert cost == 1


def test_get_entitlement_for_date():
    entitlement = make_entitlement(amount=100)
    assert entitlement.get_entitlement_on_date(date(2026, 1, 1)) == 100


@pytest.mark.parametrize(
    "on_date,expected",
    [
        pytest.param(
            date(2025, 4, 1), 50, id="Date is within the first amount exception"
        ),
        pytest.param(date(2026, 4, 1), 273, id="Date is between the amount exceptions"),
        pytest.param(
            date(2027, 4, 1), 94, id="Date is within the second amount exception"
        ),
        pytest.param(date(2025, 3, 31), 273, id="Date is before the first exception"),
        pytest.param(date(2026, 5, 1), 273, id="Date is before the second exception"),
        pytest.param(date(2028, 4, 1), 273, id="Date is after the second exception"),
    ],
)
def test_amount_exception_applied(on_date, expected):
    # Given an entitlement with two amount exceptions
    entitlement = make_entitlement(
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
    # When the entitlement is requested for a date,
    # Then the amount exception should be applied
    assert entitlement.get_entitlement_on_date(on_date) == expected


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
    renewal_month, starting_year, expected_string
):
    # Given an entitlement that starts on the given renewal month
    entitlement = make_entitlement(renewal_month=renewal_month)
    # When the description of the year is requested
    description = entitlement.get_description_of_entitlement_for_year_starting_in(
        starting_year
    )
    # Then the description should be the expected string
    assert description == expected_string
