from datetime import datetime, timezone


def date_string_to_time_passed(prev_date: str) -> str:
    """
    Converts a date string to time passed. eg. 2 minutes ago, 1 hour ago, yesterday, 2 days ago, 2 weeks ago, etc.
    """
    now = datetime.now(timezone.utc)
    then = datetime.strptime(prev_date, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=timezone.utc
    )

    diff = now - then
    seconds = diff.total_seconds()

    if seconds < 0:
        return "in the future"

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
