from datetime import datetime

from swingmusic.db.userdata import ScrobbleTable
from swingmusic.models.playlist import Playlist
from swingmusic.lib.playlistlib import get_first_4_images
from swingmusic.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
)

from swingmusic.store.tracks import TrackStore


def get_recently_played_playlist(limit: int = 100):
    playlist = Playlist(
        id="recentlyplayed",
        name="Recently Played",
        image=None,
        last_updated="Now",
        settings={},
        trackhashes=[],
    )

    scrobbles = ScrobbleTable.get_all(None, 100)
    tracks = TrackStore.get_tracks_by_trackhashes(
        [scrobble.trackhash for scrobble in scrobbles]
    )

    date = datetime.fromtimestamp(tracks[0].lastplayed)
    playlist._last_updated = date_string_to_time_passed(create_new_date(date))

    images = get_first_4_images(tracks=tracks)
    playlist.images = images

    return playlist, tracks
