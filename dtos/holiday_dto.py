from datetime import datetime

from pydantic import BaseModel, model_validator

from holiday import Holiday


class HolidayDto(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def end_date_must_be_on_or_after_start_date(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date")
        return self

    def to_holiday(self) -> 'Holiday':
        return Holiday(start_date=self.start_date, end_date=self.end_date)
    