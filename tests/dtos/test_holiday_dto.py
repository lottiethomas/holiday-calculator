from datetime import datetime

import pytest
from pydantic import ValidationError

from dtos.holiday_dto import HolidayDto


@pytest.mark.parametrize("model",
                         [
                             {},
                             {'start_date': '2026-01-01'},
                             {'end_date': '2026-01-01'},
                         ])
def test_holiday_must_have_start_and_end_date(model):
    # Given a holiday without a start and end date
    # When the holiday is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayDto.model_validate(model)


def test_end_date_not_before_start_date():
    # Given a holiday where the end date is before the start date
    # When the holiday is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayDto.model_validate({'start_date': '2026-01-01', 'end_date': '2025-12-31'})


@pytest.mark.parametrize("model",
                         [
                             {'start_date': '2026-01-01', 'end_date': '2026-01-01'},
                             {'start_date': '2026-01-01', 'end_date': '2026-01-02'},
                         ])
def test_end_date_can_be_on_or_after_start_date(model):
    # Given a holiday where the end date is after the start date
    # When the holiday is created,
    # No validation exception should be thrown
    HolidayDto.model_validate(model)


def test_dto_can_be_converted_to_holiday():
    description = 'test holiday'
    # Given a holiday DTO
    holiday_dto = HolidayDto.model_validate(
        {'start_date': '2026-01-01', 'end_date': '2026-01-02', 'description': description})
    # When the DTO is converted to a holiday,
    holiday = holiday_dto.to_holiday()
    # Then the holiday should have the correct start and end date, and description
    assert holiday.start_date == datetime(2026, 1, 1)
    assert holiday.end_date == datetime(2026, 1, 2)
    assert holiday.description == description


def test_dto_can_be_converted_to_holiday_without_description():
    # Given a holiday DTO without a description
    holiday_dto = HolidayDto.model_validate(
        {'start_date': '2026-01-01', 'end_date': '2026-01-02'})
    # When the DTO is converted to a holiday,
    holiday = holiday_dto.to_holiday()
    # Then the holiday should have the correct start and end date, and the default description
    assert holiday.start_date == datetime(2026, 1, 1)
    assert holiday.end_date == datetime(2026, 1, 2)
    assert holiday.description == ""
