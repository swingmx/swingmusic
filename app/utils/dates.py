import pendulum
from datetime import datetime

_format = "%Y-%m-%d %H:%M:%S"


def create_new_date(date: datetime = None) -> str:
    """
    Creates a new date and time string in the format of "YYYY-MM-DD HH:MM:SS"
    :return: A string of the current date and time.
    """
    if not date:
        date = datetime.now()

    return date.strftime(_format)


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. e.g. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """
    now = datetime.now().timestamp()
    then = datetime.strptime(prev_date, _format).timestamp()

    diff = now - then
    now = pendulum.now()
    return now.subtract(seconds=diff).diff_for_humans()
