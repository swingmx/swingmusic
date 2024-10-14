from dataclasses import dataclass
from gettext import ngettext
from itertools import groupby
from math import e
from pprint import pprint
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
import pendulum
from pydantic import Field, BaseModel
from app.api.apischemas import TrackHashSchema
from typing import Literal
from datetime import datetime, timedelta
from collections import defaultdict
import locale

from app.db.userdata import FavoritesTable, ScrobbleTable
from app.lib.extras import get_extra_info
from app.models.album import Album
from app.models.stats import StatItem
from app.models.track import Track
from app.serializers.artist import serialize_for_card
from app.serializers.album import serialize_for_card as serialize_for_album_card
from app.serializers.track import serialize_track, serialize_tracks
from app.settings import Defaults
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.dates import (
    get_date_range,
    get_duration_in_seconds,
    seconds_to_time_string,
)
from app.utils.stats import (
    calculate_album_trend,
    calculate_artist_trend,
    calculate_new_albums,
    calculate_new_artists,
    calculate_scrobble_trend,
    calculate_track_trend,
    get_albums_in_period,
    get_artists_in_period,
    get_tracks_in_period,
)

bp_tag = Tag(name="Logger", description="Log item plays")
api = APIBlueprint("logger", __name__, url_prefix="/logger", abp_tags=[bp_tag])


class LogTrackBody(TrackHashSchema):
    timestamp: int = Field(description="The timestamp of the track", example=1622217600)
    duration: int = Field(
        description="The duration of the track in seconds", example=300
    )
    source: str = Field(
        description="The play source of the track",
        example=f"al:{Defaults.API_ALBUMHASH}",
    )


def format_date(start: float, end: float):
    return f"{pendulum.from_timestamp(start).format('MMM D, YYYY')} - {pendulum.from_timestamp(end).format('MMM D, YYYY')}"


@api.post("/track/log")
def log_track(body: LogTrackBody):
    """
    Log a track play to the database.
    """
    timestamp = body.timestamp
    duration = body.duration

    if not timestamp or duration < 5:
        return {"msg": "Invalid entry."}, 400

    trackentry = TrackStore.trackhashmap.get(body.trackhash)
    if trackentry is None:
        return {"msg": "Track not found."}, 404

    scrobble_data = dict(body)
    scrobble_data["extra"] = get_extra_info(body.trackhash, "track")
    ScrobbleTable.add(scrobble_data)

    # Update play data on the in-memory stores
    track = trackentry.tracks[0]
    album = AlbumStore.albummap.get(track.albumhash)

    if album:
        album.increment_playcount(duration, timestamp)

    for hash in track.artisthashes:
        artist = ArtistStore.artistmap.get(hash)

        if artist:
            artist.increment_playcount(duration, timestamp)

    track = TrackStore.trackhashmap.get(body.trackhash)
    if track:
        track.increment_playcount(duration, timestamp)

    return {"msg": "recorded"}, 201


class ChartItemsQuery(BaseModel):
    duration: Literal["week", "month", "year", "alltime"] = Field(
        "year",
        description="Duration to fetch data for",
    )
    limit: int = Field(10, description="Number of top tracks to return")
    order_by: Literal["playcount", "playduration"] = Field(
        "playduration", description="Property to order by"
    )


# SECTION: STATS


def get_help_text(
    playcount: int, playduration: int, order_by: Literal["playcount", "playduration"]
):
    """
    Get the help text given the playcount and playduration.
    """
    if order_by == "playcount":
        if playcount == 0:
            return "unplayed"

        return f"{playcount} play{'' if playcount == 1 else 's'}"
    if order_by == "playduration":
        return seconds_to_time_string(playduration)


# DISCLAIMER: Code beyond this point was partially written by Claude 3.5 Sonnet in Cursor.
# TODO: Refactor, group and clean up


@api.get("/top-tracks")
def get_top_tracks(query: ChartItemsQuery):
    """
    Get the top N tracks played within a given duration.
    """
    start_time, end_time = get_date_range(query.duration)
    previous_start_time = start_time - get_duration_in_seconds(query.duration)

    current_period_tracks, current_period_scrobbles, duration = get_tracks_in_period(
        start_time, end_time
    )
    previous_period_tracks, previous_period_scrobbles, _ = get_tracks_in_period(
        previous_start_time, start_time
    )
    scrobble_trend = (
        "rising"
        if current_period_scrobbles > previous_period_scrobbles
        else (
            "falling"
            if current_period_scrobbles < previous_period_scrobbles
            else "stable"
        )
    )

    sorted_tracks = sort_tracks(current_period_tracks, query.order_by)
    top_tracks = sorted_tracks[: query.limit]

    response = []
    for track in top_tracks:
        trend = calculate_track_trend(
            track, current_period_tracks, previous_period_tracks
        )
        track = {
            **serialize_track(track),
            "trend": trend,
            "help_text": get_help_text(
                track.playcount, track.playduration, query.order_by
            ),
        }

        response.append(track)

    return {
        "tracks": response,
        "scrobbles": {
            "text": f"{current_period_scrobbles} total play{'' if current_period_scrobbles == 1 else 's'} ({seconds_to_time_string(duration)})",
            "trend": scrobble_trend,
            "dates": format_date(start_time, end_time),
        },
    }, 200


def sort_tracks(tracks: list[Track], order_by: Literal["playcount", "playduration"]):
    return sorted(tracks, key=lambda x: getattr(x, order_by), reverse=True)


@api.get("/top-artists")
def get_top_artists(query: ChartItemsQuery):
    """
    Get the top N artists played within a given duration.
    """
    start_time, end_time = get_date_range(query.duration)
    previous_start_time = start_time - get_duration_in_seconds(query.duration)

    current_period_artists = get_artists_in_period(start_time, end_time)
    previous_period_artists = get_artists_in_period(previous_start_time, start_time)

    new_artists = calculate_new_artists(current_period_artists, start_time)
    scrobble_trend = calculate_scrobble_trend(
        len(current_period_artists), len(previous_period_artists)
    )

    sorted_artists = sort_artists(current_period_artists, query.order_by)
    top_artists = sorted_artists[: query.limit]

    response = []
    for artist in top_artists:
        trend = calculate_artist_trend(
            artist, current_period_artists, previous_period_artists
        )
        db_artist = ArtistStore.get_artist_by_hash(artist["artisthash"])

        if db_artist is None:
            continue

        artist = {
            **serialize_for_card(db_artist),
            "trend": trend,
            "help_text": get_help_text(
                artist["playcount"], artist["playduration"], query.order_by
            ),
            "extra": {
                "playcount": artist["playcount"],
            },
        }
        response.append(artist)

    return {
        "artists": response,
        "scrobbles": {
            "text": f"{new_artists} {'new' if query.duration != 'alltime' else ''} {ngettext('artist', 'artists', new_artists)}",
            "trend": scrobble_trend,
            "dates": format_date(start_time, end_time),
        },
    }, 200


def sort_artists(artists, order_by):
    return sorted(artists, key=lambda x: x[order_by], reverse=True)


@api.get("/top-albums")
def get_top_albums(query: ChartItemsQuery):
    """
    Get the top N albums played within a given duration.
    """
    start_time, end_time = get_date_range(query.duration)
    previous_start_time = start_time - get_duration_in_seconds(query.duration)

    current_period_albums = get_albums_in_period(start_time, end_time)
    previous_period_albums = get_albums_in_period(previous_start_time, start_time)

    new_albums = calculate_new_albums(current_period_albums, previous_period_albums)
    scrobble_trend = calculate_scrobble_trend(
        len(current_period_albums), len(previous_period_albums)
    )

    sorted_albums = sort_albums(current_period_albums, query.order_by)
    top_albums = sorted_albums[: query.limit]

    response = []
    for album in top_albums:
        trend = calculate_album_trend(
            album, current_period_albums, previous_period_albums
        )
        album = {
            **serialize_for_album_card(album),
            "trend": trend,
            "help_text": get_help_text(
                album.playcount, album.playduration, query.order_by
            ),
        }
        response.append(album)

    return {
        "albums": response,
        "scrobbles": {
            "text": f"{new_albums} new album{'' if new_albums == 1 else 's'} played",
            "trend": scrobble_trend,
            "dates": format_date(start_time, end_time),
        },
    }, 200


def sort_albums(albums: list[Album], order_by: Literal["playcount", "playduration"]):
    return sorted(albums, key=lambda x: getattr(x, order_by), reverse=True)


@api.get("/stats")
def get_stats():
    """
    Get the stats for the user.
    """
    period = "week"
    start_time, end_time = get_date_range(period)

    said_period = period
    match period:
        case "week":
            said_period = "this week"
        case "month":
            said_period = "this month"
        case "year":
            said_period = "this year"
        case "alltime":
            said_period = "all time"

    count = len(TrackStore.get_flat_list())
    total_tracks = StatItem(
        "trackcount",
        "in your library",
        locale.format_string("%d", count, grouping=True)
        + " "
        + ngettext("track", "tracks", count),
    )

    tracks, playcount, playduration = get_tracks_in_period(start_time, end_time)

    playcount = StatItem(
        "streams",
        said_period,
        f"{playcount} track {ngettext('play', 'plays', playcount)}",
    )

    playduration = StatItem(
        "playtime",
        said_period,
        f"{seconds_to_time_string(playduration)} listened",
    )

    tracks = sorted(tracks, key=lambda t: t.playduration, reverse=True)

    # Find the top track from the last 7 days
    top_track = StatItem(
        "toptrack",
        f"Top track {said_period}",
        (
            tracks[0].title + " - " + tracks[0].artists[0]["name"]
            if len(tracks) > 0
            else "—"
        ),
        tracks[0].image if len(tracks) > 0 else None,
    )

    fav_count = FavoritesTable.count_favs_in_period(start_time, end_time)
    favorites = StatItem(
        "favorites",
        said_period,
        f"{fav_count} {'new' if period != 'alltime' else ''} favorite{'' if fav_count == 1 else 's'}",
    )

    return {
        "stats": [
            top_track,
            playcount,
            playduration,
            favorites,
            total_tracks,
        ],
        "dates": format_date(start_time, end_time),
    }, 200
