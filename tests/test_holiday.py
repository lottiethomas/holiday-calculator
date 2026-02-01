from datetime import datetime

from holiday import Holiday


def test_dates_in_single_day_holiday():
    holiday = Holiday.model_validate({'start_date': '2026-01-01', 'end_date': '2026-01-01'})
    dates = holiday.get_dates_in_holiday()
    assert len(dates) == 1
    assert dates[0] == datetime(2026, 1, 1)


def test_dates_in_multiple_day_holiday():
    holiday = Holiday.model_validate({'start_date': '2026-01-01', 'end_date': '2026-01-03'})
    dates = holiday.get_dates_in_holiday()
    assert len(dates) == 3
    assert dates[0] == datetime(2026, 1, 1)
    assert dates[1] == datetime(2026, 1, 2)
    assert dates[2] == datetime(2026, 1, 3)
