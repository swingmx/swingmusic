from typing import Any
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
    items_map: dict[str, Any] = {}

    BATCH_SIZE = 200
    current_index = 0

    # if entries are provided, return 1 item
    if len(_entries):
        entries = _entries
        limit = 1
    else:
        entries = ScrobbleTable.get_all(0, BATCH_SIZE, userid=userid)

    max_iterations = 20
    iterations = 0

    def return_items():
        """
        Return a list of items sorted by timestamp in descending order.
        """
        return sorted(items_map.values(), key=lambda x: x["timestamp"], reverse=True)

    while len(items_map.keys()) < limit and iterations < max_iterations:
        items = create_items(entries, limit)

        if not len(items):
            break

        for item in items:
            if item["hash"] in items_map:
                continue

            items_map[item["hash"]] = item

            if len(items_map.keys()) >= limit:
                return return_items()

        current_index += BATCH_SIZE

        if len(items_map.keys()) < limit and not len(_entries):
            entries = ScrobbleTable.get_all(
                start=current_index, limit=BATCH_SIZE, userid=userid
            )

        iterations += 1

    return return_items()
