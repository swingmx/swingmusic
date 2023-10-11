import pendulum
from datetime import datetime

_format = "%Y-%m-%d %H:%M:%S"


def create_new_date():
    """
    Creates a new date and time string in the format of "YYYY-MM-DD HH:MM:SS"
    :return: A string of the current date and time.
    """
    now = datetime.now()
    return now.strftime(_format)


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. e.g. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """
    now = datetime.now()
    then = datetime.strptime(prev_date, _format)

    diff = now - then
    seconds = diff.seconds

    now = pendulum.now()
    return now.subtract(seconds=seconds).diff_for_humans()

