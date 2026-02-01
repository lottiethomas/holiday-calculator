from datetime import datetime
from pydantic import BaseModel
import pandas as pd


class Holiday(BaseModel):
    start_date: datetime
    end_date: datetime

    def get_dates_in_holiday(self) -> pd.DatetimeIndex:
        return pd.date_range(self.start_date, self.end_date, freq='D')
