from swingmusic.db.userdata import ScrobbleTable
from swingmusic.lib.home.create_items import create_items
from swingmusic.models.logger import TrackLog


def get_recently_played(
    limit: int, userid: int | None = None, _entries: list[TrackLog] = []
):
    """
    Get the recently played items for the homepage.

    Pass a list of track log entries to use a subset of the scrobble table.
    """
    # TODO: Paginate this
    items = []

    BATCH_SIZE = 200
    current_index = 0

    if len(_entries):
        entries = _entries
        limit = 1
    else:
        entries = ScrobbleTable.get_all(0, BATCH_SIZE, userid=userid)

    max_iterations = 20
    iterations = 0

    while len(items) < limit and iterations < max_iterations:
        items.extend(create_items(entries, limit))
        current_index += BATCH_SIZE

        if len(items) < limit:
            entries = ScrobbleTable.get_all(
                start=current_index + 1, limit=BATCH_SIZE, userid=userid
            )
            if not entries:
                break

        iterations += 1

    return items