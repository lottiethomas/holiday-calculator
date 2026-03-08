from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, model_validator, Field

from amount_exception import AmountException


class AmountExceptionDto(BaseModel):
    start_date: datetime
    end_date: datetime
    amount: Annotated[float, Field(ge=0)]

    @model_validator(mode='after')
    def end_date_must_be_after_start_date(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return self

    def to_amount_exception(self) -> AmountException:
        return AmountException(start_date=self.start_date, end_date=self.end_date, amount=self.amount)