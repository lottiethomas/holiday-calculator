from datetime import datetime

from holiday import Holiday


def test_dates_in_single_day_holiday():
    # Given a single day holiday
    holiday = Holiday(start_date=datetime(2026, 1, 1), end_date=datetime(2026, 1, 1))
    # When the holiday is converted to a list of dates
    dates = holiday.get_dates_in_holiday()
    # Then the list should contain only the single date
    assert len(dates) == 1
    # And the date should be the same as the start date and end date
    assert dates[0] == datetime(2026, 1, 1)


def test_dates_in_multiple_day_holiday():
    # Given a holiday spanning three days
    holiday = Holiday(start_date=datetime(2026, 1, 1), end_date=datetime(2026, 1, 3))
    # When the holiday is converted to a list of dates
    dates = holiday.get_dates_in_holiday()
    # Then the list should contain the three dates
    assert len(dates) == 3
    # And the dates should be the three dates in the correct order
    assert dates[0] == datetime(2026, 1, 1)
    assert dates[1] == datetime(2026, 1, 2)
    assert dates[2] == datetime(2026, 1, 3)
