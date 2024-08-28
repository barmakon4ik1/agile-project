from datetime import datetime
import calendar
from django.utils import timezone


def calculate_end_of_month() -> datetime:
    current_date = timezone.now()
    amount_of_days = calendar.monthrange(
        current_date.year,
        current_date.month)[1]
    date = datetime(
        year=current_date.year,
        month=current_date.month,
        day=amount_of_days,
    )
    return date.astimezone()
