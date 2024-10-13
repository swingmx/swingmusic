import pendulum
from datetime import datetime, timedelta

_format = "%Y-%m-%d %H:%M:%S"


def timestamp_from_days_ago(days_ago: int):
    """
    Returns a timestamp from a number of days ago.
    """
    current_datetime = datetime.now()
    delta = timedelta(days=days_ago)
    past_timestamp = current_datetime - delta

    return int(past_timestamp.timestamp())


def create_new_date(date: datetime = None) -> str:
    """
    Creates a new date and time string in the format of "YYYY-MM-DD HH:MM:SS"
    :return: A string of the current date and time.
    """
    if not date:
        date = datetime.now()

    return date.strftime(_format)


def timestamp_to_time_passed(timestamp: str | int):
    """
    Converts a timestamp to time passed. e.g. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """
    now = datetime.now().timestamp()
    then = datetime.fromtimestamp(int(timestamp)).timestamp()

    diff = now - then
    now = pendulum.now()
    return now.subtract(seconds=diff).diff_for_humans()


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. e.g. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """
    then = datetime.strptime(prev_date, _format).timestamp()
    return timestamp_to_time_passed(then)


def seconds_to_time_string(seconds):
    """
    Converts seconds to a time string. e.g. 1 hour 2 minutes, 1 hour 2 seconds, 1 hour, 1 minute 2 seconds, etc.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        if minutes > 0:
            return f"{hours} hr{'s' if hours > 1 else ''}, {minutes} min{'s' if minutes > 1 else ''}"

        return f"{hours} hr{'s' if hours > 1 else ''}"

    if minutes > 0:
        return f"{minutes} min{'s' if minutes > 1 else ''}"

    return f"{remaining_seconds} sec"


def get_date_range(duration: str):
    """
    Returns a tuple of dates representing the start and end of a given duration.
    """
    match duration:
        case "week":
            return (
                pendulum.now().subtract().start_of("week").timestamp(),
                pendulum.now().end_of("week").timestamp(),
            )
        case "month":
            return (
                pendulum.now().subtract().start_of("month").timestamp(),
                pendulum.now().end_of("month").timestamp(),
            )
        case "year":
            return (
                pendulum.now().subtract().start_of("year").timestamp(),
                pendulum.now().end_of("year").timestamp(),
            )
        case "alltime":
            return (float(0), pendulum.now().timestamp())
        case _:
            raise ValueError(f"Invalid duration: {duration}")


def get_duration_in_seconds(duration: str) -> float:
    """
    Returns the number of seconds in a given duration.
    """
    match duration:
        case "week":
            return 604800
        case "month":
            return 2629743
        case "year":
            return 31556926
        case "alltime":
            return pendulum.now().timestamp()

    raise ValueError(f"Invalid duration: {duration}")
