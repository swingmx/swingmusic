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


def seconds_to_time_string(seconds):
    """
    Converts seconds to a time string. e.g. 1 hour 2 minutes, 1 hour 2 seconds, 1 hour, 1 minute 2 seconds, etc.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} hr{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"

        return f"{hours} hr{'s' if hours > 1 else ''}"

    if minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''}"

    return f"{remaining_seconds} second{'s' if remaining_seconds > 1 else ''}"
