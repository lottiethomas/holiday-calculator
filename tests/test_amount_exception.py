from datetime import date

import pytest

from holiday_calculator.amount_exception import AmountException


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (date(2026, 1, 2), date(2026, 1, 1)),
        (date(2026, 1, 2), date(2026, 1, 2)),
    ],
)
def test_end_date_must_be_after_start_date(start_date, end_date):
    # Given an amount exception where the end date is on or before the start date
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValueError):
        AmountException(start_date, end_date, 5)
