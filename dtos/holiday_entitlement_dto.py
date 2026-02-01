from typing import Tuple, Annotated, Optional

from pydantic import BaseModel, model_validator, Field

from dtos.amount_exception_dto import AmountExceptionDto
from entitlement_counting_method import EntitlementCountingMethod
from holiday_entitlement import HolidayEntitlement


class HolidayEntitlementDto(BaseModel):
    counting_method: EntitlementCountingMethod
    amount: float
    bank_holidays_counted: bool
    working_pattern: Tuple[float, float, float, float, float, float, float]
    renewal_month: Annotated[int, Field(ge=1, le=12)]
    amount_exceptions: Optional[list[AmountExceptionDto]] = None

    @model_validator(mode='after')
    def amount_must_be_less_than_a_year(self):
        if self.counting_method is EntitlementCountingMethod.DAYS and self.amount > 366:
            raise ValueError("Amount must not exceed a year")
        if self.counting_method is EntitlementCountingMethod.HOURS and self.amount > 8784:
            raise ValueError("Amount must not exceed a year")
        return self

    @model_validator(mode='after')
    def validate_working_pattern(self):
        if len(self.working_pattern) != 7:
            raise ValueError('Working pattern does not have 7 elements')
        for day in self.working_pattern:
            if day < 0:
                raise ValueError('Each day in the working pattern must be non-negative')
            if self.counting_method is EntitlementCountingMethod.DAYS:
                if day > 1:
                    raise ValueError('When the counting method is DAYS, '
                                     'each day in the working pattern may not exceed 1')
            if self.counting_method is EntitlementCountingMethod.HOURS:
                if day > 24:
                    raise ValueError('When the counting method is HOURS, '
                                     'each day in the working pattern may not exceed 24')
        return self

    def to_holiday_entitlement(self) -> HolidayEntitlement:
        return HolidayEntitlement(counting_method=self.counting_method,
                                  amount=self.amount,
                                  bank_holidays_counted=self.bank_holidays_counted,
                                  working_pattern=self.working_pattern,
                                  renewal_month=self.renewal_month,
                                  amount_exceptions=[exception.to_amount_exception() for exception in
                                                     self.amount_exceptions] if self.amount_exceptions is not None else None)
