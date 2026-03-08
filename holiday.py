from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class Holiday:
    start_date: datetime
    end_date: datetime

    def get_dates_in_holiday(self) -> pd.DatetimeIndex:
        return pd.date_range(self.start_date, self.end_date, freq='D')
