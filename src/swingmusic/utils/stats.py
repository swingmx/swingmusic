from collections import defaultdict
import copy

from typing import Any, Callable, TypeVar, List
from swingmusic.db.userdata import ScrobbleTable
from swingmusic.models.stats import StatItem
from swingmusic.models.track import Track
from swingmusic.models.album import Album
from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.dates import seconds_to_time_string


def get_artists_in_period(
    start_time: int | float, end_time: int | float, userid: int | None = None
):
    scrobbles = ScrobbleTable.get_all_in_period(start_time, end_time, userid)
    artists: Any = defaultdict(
        lambda: {"playcount": 0, "playduration": 0, "tracks": {}}
    )

    for scrobble in scrobbles:
        track = TrackStore.get_tracks_by_trackhashes([scrobble.trackhash])
        if not track:
            continue

        track = track[0]

        for artist in track.artists:
            artisthash = artist["artisthash"]

            artists[artisthash]["artist"] = artist["name"]
            artists[artisthash]["artisthash"] = artist["artisthash"]
            artists[artisthash]["playcount"] += 1
            artists[artisthash]["playduration"] += scrobble.duration

            # index the track counts too
            artists[artisthash]["tracks"][track.trackhash] = (
                artists[artisthash]["tracks"].get(track.trackhash, 0) + 1
            )

    artists = list(artists.values())
    return sorted(artists, key=lambda x: x["playduration"], reverse=True)


def get_albums_in_period(start_time: int, end_time: int, userid: int | None = None):
    scrobbles = ScrobbleTable.get_all_in_period(start_time, end_time, userid)
    albums: dict[str, Album] = {}

    for scrobble in scrobbles:
        track = TrackStore.get_tracks_by_trackhashes([scrobble.trackhash])
        if not track:
            continue

        track = track[0]
        album_entry = AlbumStore.albummap.get(track.albumhash)
        if not album_entry:
            continue
        album_entry = copy.deepcopy(album_entry)

        albumhash = album_entry.album.albumhash
        if albumhash not in albums:
            albums[albumhash] = album_entry.album
            albums[albumhash].playcount = 0
            albums[albumhash].playduration = 0

        albums[albumhash].playcount += 1
        albums[albumhash].playduration += scrobble.duration

    return list(albums.values())


def get_tracks_in_period(start_time: int, end_time: int, userid: int | None = None):
    scrobbles = ScrobbleTable.get_all_in_period(start_time, end_time, userid)
    tracks: dict[str, Track] = {}
    duration = 0

    total = 0

    for scrobble in scrobbles:
        total += 1
        if scrobble.trackhash not in tracks:
            try:
                track = copy.deepcopy(
                    TrackStore.get_tracks_by_trackhashes([scrobble.trackhash])[0]
                )
            except IndexError:
                continue

            tracks[scrobble.trackhash] = track
            tracks[scrobble.trackhash].playcount = 0
            tracks[scrobble.trackhash].playduration = 0

        tracks[scrobble.trackhash].playcount += 1
        tracks[scrobble.trackhash].playduration += scrobble.duration
        duration += scrobble.duration

    return list(tracks.values()), total, duration


T = TypeVar("T")


def calculate_trend(
    item: T,
    current_items: List[T],
    previous_items: List[T],
    key_func: Callable[[T], Any],
):
    """
    Calculate the trend of an item based on its position in current and previous lists.

    :param item: The item to calculate the trend for
    :param current_items: The current list of items
    :param previous_items: The previous list of items
    :param key_func: A function to extract the comparison key from an item
    :return: A dictionary containing:
             - The trend as a string: 'rising', 'falling', or 'stable'
             - A boolean flag indicating whether the item is new
    """
    current_rank = next(
        (i for i, t in enumerate(current_items) if key_func(t) == key_func(item)), -1
    )
    previous_rank = next(
        (i for i, t in enumerate(previous_items) if key_func(t) == key_func(item)), -1
    )

    is_new = previous_rank == -1

    if is_new:
        return {"trend": "rising", "is_new": True}
    elif current_rank == -1:
        return {"trend": "falling", "is_new": False}
    elif current_rank < previous_rank:
        return {"trend": "rising", "is_new": False}
    elif current_rank > previous_rank:
        return {"trend": "falling", "is_new": False}
    else:
        return {"trend": "stable", "is_new": False}


def calculate_album_trend(
    album_entry: Album, current_albums: List[Album], previous_albums: List[Album]
):
    return calculate_trend(
        album_entry, current_albums, previous_albums, lambda a: a.albumhash
    )


def calculate_artist_trend(
    artist: dict[str, Any],
    current_artists: List[dict[str, Any]],
    previous_artists: List[dict[str, Any]],
):
    return calculate_trend(
        artist, current_artists, previous_artists, lambda a: a["artisthash"]
    )


def calculate_track_trend(
    track: Track, current_tracks: List[Track], previous_tracks: List[Track]
):
    return calculate_trend(
        track, current_tracks, previous_tracks, lambda t: t.trackhash
    )


def calculate_scrobble_trend(current_scrobbles: int, previous_scrobbles: int) -> str:
    return (
        "rising"
        if current_scrobbles > previous_scrobbles
        else ("falling" if current_scrobbles < previous_scrobbles else "stable")
    )


def calculate_new_artists(
    current_artists: List[dict[str, Any]], timestamp: int, userid: int | None = None
):
    """
    Calculate the number of new artists based on the current and all previous scrobbles.
    """
    current_artists_set = set(artist["artisthash"] for artist in current_artists)
    all_records = ScrobbleTable.get_all_in_period(0, timestamp, userid)
    trackhashes = set(record.trackhash for record in all_records)

    previous_artists_set = set()

    for record in trackhashes:
        entry = TrackStore.trackhashmap.get(record)
        if not entry:
            continue

        entry = entry.tracks[0]

        for artist in entry.artists:
            artisthash = artist["artisthash"]
            previous_artists_set.add(artisthash)

    return len(current_artists_set - previous_artists_set)


def calculate_new_albums(current_albums: List[Album], previous_albums: List[Album]):
    current_albums_set = set(album.albumhash for album in current_albums)
    previous_albums_set = set(album.albumhash for album in previous_albums)

    return len(current_albums_set - previous_albums_set)


def get_track_group_stats(tracks: list[Track], is_album: bool = False):
    if len(tracks) == 0:
        return []

    played_tracks = [track for track in tracks if track.playcount > 0]
    unplayed_count = len(tracks) - len(played_tracks)

    played_stat = StatItem(
        "played",
        f"never played",
        f"{unplayed_count}/{len(tracks)} tracks",
    )

    play_duration = sum(track.playduration for track in played_tracks)
    play_duration_stat = StatItem(
        "play_duration",
        "listened all time",
        f"{seconds_to_time_string(play_duration)}",
    )

    try:
        top_track = max(played_tracks, key=lambda x: x.playduration)
    except ValueError:
        top_track = None

    top_track_stat = (
        StatItem(
            "toptrack",
            f"top track ({seconds_to_time_string(top_track.playduration)} listened)",
            f"{top_track.title}",
            top_track.image if top_track else None,
        )
        if top_track
        else StatItem(
            "toptrack",
            "top track",
            "—",
        )
    )

    albums_map = {}

    for track in tracks:
        if track.albumhash not in albums_map:
            albums_map[track.albumhash] = {
                "playcount": 0,
                "playduration": 0,
                "title": track.album,
                "image": track.image if track.image else None,
            }

        albums_map[track.albumhash]["playcount"] += 1
        albums_map[track.albumhash]["playduration"] += track.playduration

    stats = [play_duration_stat, played_stat, top_track_stat]
    if not is_album:
        albums = list(albums_map.values())
        albums.sort(key=lambda x: x["playduration"], reverse=True)

        top_album = albums[0] if albums[0]["playduration"] else None
        top_album_stat = (
            StatItem(
                "topalbum",
                f"top album ({seconds_to_time_string(top_album['playduration'])} listened)",
                f"{top_album['title']}",
                top_album["image"])
            if top_album
            else StatItem(
                "topalbum",
                "top album",
                "—",
            )
        )

        stats.append(top_album_stat)

    if is_album:
        tracktotal: int = max(
            int(track.extra.get("track_total", 0) or 0) for track in tracks
        )
        percentage = (len(tracks) / tracktotal) * 100 if tracktotal > 0 else 101
        completedness = int(percentage) if percentage <= 100 else "?"

        completeness_stat = (
            StatItem(
                "completeness",
                f"{len(tracks)}/{tracktotal} tracks available",
                f"{completedness}% complete",
            )
            if tracktotal
            else StatItem(
                "completeness",
                f"{len(tracks)}/? tracks available",
                "?",
            )
        )

        stats.append(completeness_stat)

    return stats
