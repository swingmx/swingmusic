from datetime import datetime


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. eg. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """

    now = datetime.now()
    then = datetime.strptime(prev_date, "%Y-%m-%d %H:%M:%S")

    diff = now - then
    days = diff.days

    if days < 0:
        return "in the future"

    if days == 0:
        seconds = diff.seconds

        if seconds < 15:
            return "now"

        if seconds < 60:
            return str(seconds) + " seconds ago"

        if seconds < 3600:
            return str(seconds // 60) + " minutes ago"

        return str(seconds // 3600) + " hours ago"

    if days == 1:
        return "yesterday"

    if days < 7:
        return str(days) + " days ago"

    if days < 30:
        if days < 14:
            return "1 week ago"

        return str(days // 7) + " weeks ago"
    if days < 365:
        if days < 60:
            return "1 month ago"

        return str(days // 30) + " months ago"
    if days > 365:
        if days < 730:
            return "1 year ago"

        return str(days // 365) + " years ago"

    return "I honestly don't know"

