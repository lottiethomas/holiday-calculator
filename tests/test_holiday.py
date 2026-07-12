from datetime import date

import pytest

from holiday_calculator.holiday import Holiday


def holiday(start_day: int, end_day: int) -> Holiday:
    return Holiday(
        start_date=date(2026, 1, start_day),
        end_date=date(2026, 1, end_day),
    )


@pytest.mark.parametrize(
    "start_date, end_date",
    [
        (
            date(2026, 1, 1),
            date(2026, 1, 1),
        ),
        (
            date(2026, 1, 1),
            date(2026, 1, 2),
        ),
    ],
)
def test_end_date_can_be_on_or_after_start_date(start_date: date, end_date: date):
    # Given a holiday where the end date is after the start date
    # When the holiday is created,
    # No validation exception should be thrown
    Holiday(start_date, end_date)


def test_end_date_not_before_start_date():
    # Given a holiday where the end date is before the start date
    # When the holiday is created,
    # A validation exception should be thrown
    with pytest.raises(ValueError):
        Holiday(date(2026, 1, 1), date(2025, 12, 31))


@pytest.mark.parametrize(
    "holiday_start_day, holiday_end_day, from_date, to_date, expected_dates",
    [
        pytest.param(
            1,
            1,
            None,
            None,
            [date(2026, 1, 1)],
            id="single-day holiday",
        ),
        pytest.param(
            1,
            3,
            None,
            None,
            [date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)],
            id="multiple-day holiday",
        ),
        pytest.param(
            1,
            3,
            date(2026, 1, 2),
            None,
            [date(2026, 1, 2), date(2026, 1, 3)],
            id="from date specified",
        ),
        pytest.param(
            1,
            3,
            None,
            date(2026, 1, 2),
            [date(2026, 1, 1), date(2026, 1, 2)],
            id="to date specified",
        ),
        pytest.param(
            1,
            3,
            date(2026, 1, 2),
            date(2026, 1, 2),
            [date(2026, 1, 2)],
            id="from and to date specified",
        ),
        pytest.param(
            2,
            3,
            date(2026, 1, 1),
            date(2026, 1, 4),
            [date(2026, 1, 2), date(2026, 1, 3)],
            id="range extends beyond holiday",
        ),
        pytest.param(
            1,
            3,
            date(2026, 1, 4),
            None,
            [],
            id="from date after holiday end",
        ),
        pytest.param(
            1,
            3,
            None,
            date(2025, 12, 31),
            [],
            id="to date before holiday start",
        ),
    ],
)
def test_dates_in_holiday(
    holiday_start_day: int,
    holiday_end_day: int,
    from_date: date | None,
    to_date: date | None,
    expected_dates: list[date],
):
    holiday_instance = holiday(holiday_start_day, holiday_end_day)
    dates = holiday_instance.get_dates_in_holiday(
        from_date=from_date,
        to_date=to_date,
    )
    assert list(dates) == expected_dates


@pytest.mark.parametrize(
    "holiday_start_day, holiday_end_day, from_date, to_date, expected_result",
    [
        pytest.param(
            1,
            1,
            date(2026, 1, 1),
            date(2026, 1, 14),
            True,
            id="single day holiday within date range",
        ),
        pytest.param(
            1,
            5,
            date(2026, 1, 1),
            date(2026, 1, 14),
            True,
            id="multiple day holiday within date range",
        ),
        pytest.param(
            1,
            5,
            date(2026, 1, 1),
            date(2026, 1, 3),
            True,
            id="range ends before holiday end",
        ),
        pytest.param(
            1,
            5,
            date(2026, 1, 3),
            date(2026, 1, 14),
            True,
            id="range starts after holiday start",
        ),
        pytest.param(
            10,
            15,
            date(2026, 1, 3),
            date(2026, 1, 5),
            False,
            id="range ends before holiday start",
        ),
        pytest.param(
            1,
            5,
            date(2026, 1, 10),
            date(2026, 1, 15),
            False,
            id="range starts after holiday end",
        ),
        pytest.param(
            1,
            5,
            date(2025, 6, 1),
            date(2026, 5, 31),
            True,
            id="both dates within holiday year",
        ),
    ],
)
def test_holiday_is_in_date_range(
    holiday_start_day: int,
    holiday_end_day: int,
    from_date: date,
    to_date: date,
    expected_result: bool,
):
    holiday_instance = holiday(holiday_start_day, holiday_end_day)
    assert (
        holiday_instance.is_in_date_range(from_date=from_date, to_date=to_date)
        == expected_result
    )
