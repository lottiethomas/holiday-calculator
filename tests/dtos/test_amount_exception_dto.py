from datetime import datetime
from typing import Optional

import pytest
from pydantic import ValidationError

from dtos.amount_exception_dto import AmountExceptionDto

DEFAULT_START_DATE = '2022-01-01'
DEFAULT_END_DATE = '2022-12-31'
DEFAULT_AMOUNT = 10


def create_model_dict_without(field_to_miss: str) -> dict:
    if field_to_miss == 'start_date':
        return create_model_dict(start_date=None)
    if field_to_miss == 'end_date':
        return create_model_dict(end_date=None)
    if field_to_miss == 'amount':
        return create_model_dict(amount=None)
    return create_model_dict()


def create_model_dict(start_date: Optional[str] = DEFAULT_START_DATE,
                      end_date: Optional[str] = DEFAULT_END_DATE,
                      amount: Optional[float] = DEFAULT_AMOUNT) -> dict:
    return {'start_date': start_date, 'end_date': end_date, 'amount': amount}


def test_start_date_must_be_present():
    # Given an amount exception without a start date
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        AmountExceptionDto.model_validate(create_model_dict_without('start_date'))


def test_end_date_must_be_present():
    # Given an amount exception without an end date
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        AmountExceptionDto.model_validate(create_model_dict_without('end_date'))


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(start_date='2022-01-02', end_date='2022-01-01'),
                             create_model_dict(start_date='2022-01-02', end_date='2022-01-02'),
                         ])
def test_end_date_must_be_after_start_date(model):
    # Given an amount exception where the end date is on or before the start date
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        AmountExceptionDto.model_validate(model)


def test_amount_must_be_present():
    # Given an amount exception without an amount
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        AmountExceptionDto.model_validate(create_model_dict_without('amount'))


def test_amount_must_not_be_negative():
    # Given an amount exception where the amount is negative
    # When the amount exception is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        AmountExceptionDto.model_validate(create_model_dict(amount=-10))


def test_amount_may_be_zero():
    # Given an amount exception where the amount is zero
    # When the amount exception is created,
    # No validation exception should be thrown
    AmountExceptionDto.model_validate(create_model_dict(amount=0))


def test_convert_to_amount_exception():
    # Given an amount exception DTO
    amount_exception_dto = AmountExceptionDto.model_validate(create_model_dict())
    # When the DTO is converted to an amount exception,
    amount_exception = amount_exception_dto.to_amount_exception()
    # Then the amount exception should have the correct fields
    assert amount_exception.start_date == datetime.strptime(DEFAULT_START_DATE, '%Y-%m-%d')
    assert amount_exception.end_date == datetime.strptime(DEFAULT_END_DATE, '%Y-%m-%d')
    assert amount_exception.amount == DEFAULT_AMOUNT
