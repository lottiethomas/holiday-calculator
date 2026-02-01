from typing import Optional

import pytest
from pydantic import ValidationError

from dtos.amount_exception_dto import AmountExceptionDto
from dtos.holiday_entitlement_dto import HolidayEntitlementDto
from entitlement_counting_method import EntitlementCountingMethod

DEFAULT_COUNTING_METHOD = 'DAYS'
DEFAULT_AMOUNT = 100
DEFAULT_BANK_HOLIDAYS_COUNTED = False
DEFAULT_WORKING_PATTERN = (1, 1, 1, 1, 1, 1, 1)
DEFAULT_RENEWAL_MONTH = 4
DEFAULT_AMOUNT_EXCEPTION = AmountExceptionDto.model_validate(
    {'start_date': '2022-01-01', 'end_date': '2022-12-31', 'amount': 50})


def create_model_dict_without(field_to_miss: str) -> dict:
    if field_to_miss == 'counting_method':
        return create_model_dict(counting_method=None)
    if field_to_miss == 'amount':
        return create_model_dict(amount=None)
    if field_to_miss == 'bank_holidays_counted':
        return create_model_dict(bank_holidays_counted=None)
    if field_to_miss == 'working_pattern':
        return create_model_dict(working_pattern=None)
    if field_to_miss == 'renewal_month':
        return create_model_dict(renewal_month=None)
    if field_to_miss == 'amount_exceptions':
        return create_model_dict(amount_exceptions=None)
    return create_model_dict()


def create_model_dict(counting_method: Optional[str] = DEFAULT_COUNTING_METHOD,
                      amount: Optional[float] = DEFAULT_AMOUNT,
                      bank_holidays_counted: Optional[bool] = DEFAULT_BANK_HOLIDAYS_COUNTED,
                      working_pattern: Optional[tuple] = DEFAULT_WORKING_PATTERN,
                      renewal_month: Optional[int] = DEFAULT_RENEWAL_MONTH,
                      amount_exceptions: Optional[list] = [DEFAULT_AMOUNT_EXCEPTION]) -> dict:
    return {'counting_method': counting_method, 'amount': amount, 'bank_holidays_counted': bank_holidays_counted,
            'working_pattern': working_pattern, 'renewal_month': renewal_month, 'amount_exceptions': amount_exceptions}


def test_entitlement_counting_method_must_be_present():
    # Given a holiday entitlement without a counting method
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict_without('counting_method'))


def test_entitlement_counting_method_must_be_valid():
    # Given a holiday entitlement with a counting method which is not valid
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict(counting_method='INVALID'))


def test_amount_must_be_present():
    # Given a holiday entitlement without an amount
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict_without('amount'))


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(counting_method='DAYS', amount=367),
                             create_model_dict(counting_method='HOURS', amount=8785),  # hours in a leap year + 1
                         ])
def test_amount_must_be_less_than_a_year(model):
    # Given a holiday entitlement where the amount is greater than a year
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(model)


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(counting_method='DAYS', amount=365),
                             create_model_dict(counting_method='HOURS', amount=8760),  # number of hours in a year
                             create_model_dict(counting_method='DAYS', amount=366),
                             create_model_dict(counting_method='HOURS', amount=8784),  # number of hours in a leap year
                         ])
def test_amount_can_be_a_year(model):
    # Given a holiday entitlement where the amount is equal to a year
    # When the holiday entitlement is created,
    # No validation exception should be thrown
    HolidayEntitlementDto.model_validate(model)


def test_bank_holiday_flag_must_be_present():
    # Given a holiday entitlement without a bank holiday flag
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict_without('bank_holidays_counted'))


def test_working_pattern_must_be_present():
    # Given a holiday entitlement without a working pattern
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict_without('working_pattern'))


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(working_pattern=(1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)),
                         ])
def test_working_pattern_must_have_length_seven(model):
    # Given a holiday entitlement with a working pattern that is not of length 7
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(model)


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(working_pattern=(1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.1, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.1, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.1, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, 1.1, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.1,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.1, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.1, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.1, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.1, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, 24.1, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, 24.0, 24.1, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, 24.0, 24.0, 24.1,)),
                         ])
def test_working_pattern_entry_must_not_exceed_1_day(model):
    # Given a holiday entitlement with a working pattern where an entry is greater than 1 day
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(model)


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(working_pattern=(-1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, -1, 1.0, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, -1, 1.0, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, -1, 1.0, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, -1, 1.0, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, -1, 1.0,)),
                             create_model_dict(working_pattern=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(-1, 24.0, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, -1, 24.0, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, -1, 24.0, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, -1, 24.0, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, -1, 24.0, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, 24.0, -1, 24.0,)),
                             create_model_dict(counting_method='HOURS',
                                               working_pattern=(24.0, 24.0, 24.0, 24.0, 24.0, 24.0, -1,)),
                         ])
def test_working_pattern_entry_must_not_be_negative(model):
    # Given a holiday entitlement with a working pattern where an entry is less than 0
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(model)


def test_renewal_date_must_be_present():
    # Given a holiday entitlement without a renewal date
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(create_model_dict_without('renewal_month'))


@pytest.mark.parametrize("model",
                         [
                             create_model_dict(renewal_month=0),
                             create_model_dict(renewal_month=13),
                         ])
def test_renewal_month_must_be_one_to_twelve(model):
    # Given a holiday entitlement where the renewal month is not between 1 and 12
    # When the holiday entitlement is created,
    # A validation exception should be thrown
    with pytest.raises(ValidationError):
        HolidayEntitlementDto.model_validate(model)


def test_amount_exceptions_can_be_missing():
    # Given a holiday entitlement without any amount exceptions
    # When the holiday entitlement is created,
    # No validation exception should be thrown
    HolidayEntitlementDto.model_validate(create_model_dict_without('amount_exceptions'))


def test_can_be_converted_to_holiday_entitlement():
    # Given a holiday entitlement DTO
    holiday_entitlement_dto = HolidayEntitlementDto.model_validate(create_model_dict())
    # When the DTO is converted to a holiday entitlement,
    holiday_entitlement = holiday_entitlement_dto.to_holiday_entitlement()
    # Then the entitlement should have the correct fields
    assert holiday_entitlement.counting_method == EntitlementCountingMethod.DAYS
    assert holiday_entitlement.amount == DEFAULT_AMOUNT
    assert holiday_entitlement.bank_holidays_counted == DEFAULT_BANK_HOLIDAYS_COUNTED
    assert holiday_entitlement.working_pattern == DEFAULT_WORKING_PATTERN
    assert holiday_entitlement.renewal_month == DEFAULT_RENEWAL_MONTH
    assert holiday_entitlement.amount_exceptions == [DEFAULT_AMOUNT_EXCEPTION.to_amount_exception()]
