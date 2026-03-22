import calendar
from datetime import datetime, date


def start_of_month(dt: datetime = None) -> datetime:
    if dt is None:
        dt = datetime.utcnow()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def end_of_month(dt: datetime = None) -> datetime:
    if dt is None:
        dt = datetime.utcnow()
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    return dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)


def days_elapsed_this_month() -> int:
    return datetime.utcnow().day


def days_remaining_this_month() -> int:
    now = datetime.utcnow()
    last_day = calendar.monthrange(now.year, now.month)[1]
    return last_day - now.day


def date_to_datetime(d: date) -> datetime:
    return datetime(d.year, d.month, d.day)
