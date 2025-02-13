from pydantic import BaseModel, Field
from datetime import date, timedelta
from typing import List

from backend.services.holiday_service import get_holidays


class EventModel(BaseModel):
    name: str
    start_date: date
    frequency: int
    country: str
    exclude_weekends: bool = True
    exclude_holidays: bool = True
    end_date: date = date.today().replace(month=12, day=31)
    extra_invalid_dates: List[date] = []

    def generate_valid_dates(self) -> List[date]:
        valid_dates = []
        holidays = get_holidays(self.start_date.year, self.country) if self.exclude_holidays else []

        invalid_dates = set(holidays) | set(self.extra_invalid_dates)

        current_date = self.start_date
        valid_day_count = 0

        while current_date <= self.end_date:
            if self.exclude_weekends and current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue
            if current_date in invalid_dates:
                current_date += timedelta(days=1)
                continue

            if valid_day_count % self.frequency == 0:
                valid_dates.append(current_date)

            valid_day_count += 1
            current_date += timedelta(days=1)
        return valid_dates
