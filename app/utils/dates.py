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
    print(seconds)

    if seconds < 0:
        return "from the future 🛸"

    if seconds < 15:
        return "now"

    if seconds < 60:
        return f"{int(seconds)} seconds ago"

    if seconds < 3600:
        return f"{int(seconds // 60)} minutes ago"

    if seconds < 86400:
        return f"{int(seconds // 3600)} hours ago"

    days = diff.days

    if days == 1:
        return "yesterday"

    if days < 7:
        return f"{days} days ago"

    if days < 14:
        return "1 week ago"

    if days < 30:
        return f"{int(days // 7)} weeks ago"

    if days < 60:
        return "1 month ago"

    if days < 365:
        return f"{int(days // 30)} months ago"

    if days < 730:
        return "1 year ago"

    return f"{int(days // 365)} years ago"
