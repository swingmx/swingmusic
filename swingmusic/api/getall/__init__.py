# swingmusic/api/getall/__init__.py (Updated)
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from datetime import datetime
from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.albumartists import AlbumArtistStore

from swingmusic.serializers.album import serialize_for_card as serialize_album
from swingmusic.serializers.artist import serialize_for_card as serialize_artist
from swingmusic.utils import format_number
from swingmusic.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
    seconds_to_time_string,
    timestamp_to_time_passed,
)
from swingmusic.utils.article_utils import get_sort_key

bp_tag = Tag(name="Get all", description="List all items")
api = APIBlueprint("getall", __name__, url_prefix="/getall", abp_tags=[bp_tag])


class GetAllItemsQuery(GenericLimitSchema):
    start: int = Field(
        description="The start index of the items to return",
        example=0,
        default=0,
    )
    sortby: str = Field(
        description="The key to sort items by",
        example="created_date",
        default="created_date",
    )

    reverse: str = Field(
        description="Reverse the sort",
        example=1,
        default="1",
    )


class GetAllItemsPath(BaseModel):
    itemtype: str = Field(
        description="The type of items to return (albums | artists | albumartists)",
        example="albums",
        default="albums",
    )


@api.get("/<itemtype>")
def get_all_items(path: GetAllItemsPath, query: GetAllItemsQuery):
    """
    Get all items

    Used to show all albums, artists, or album artists in the library

    Sort keys:
   Both albums and artists: `duration`, `created_date`, `playcount`, `playduration`, `lastplayed`, `trackcount`

    Albums only: `title`, `albumartists`, `date`
    Artists only: `name`, `albumcount`
    Album Artists only: `name`, `albumcount`
    """
    is_albums = path.itemtype == "albums"
    is_artists = path.itemtype == "artists"
    is_album_artists = path.itemtype == "albumartists"

    if is_albums:
        items = AlbumStore.get_flat_list()
    elif is_artists:
        items = ArtistStore.get_flat_list()
    elif is_album_artists:
        items = AlbumArtistStore.get_flat_list()
    else:
        return {"error": "Invalid item type. Must be 'albums', 'artists', or 'albumartists'"}, 400

    total = len(items)

    start = query.start
    limit = query.limit
    sort = query.sortby
    reverse = query.reverse == "1"

    sort_is_count = sort == "trackcount"
    sort_is_duration = sort == "duration"
    sort_is_create_date = sort == "created_date"
    sort_is_playcount = sort == "playcount"
    sort_is_playduration = sort == "playduration"
    sort_is_lastplayed = sort == "lastplayed"

    sort_is_date = is_albums and sort == "date"
    sort_is_artist = is_albums and sort == "albumartists"

    sort_is_artist_trackcount = (is_artists or is_album_artists) and sort == "trackcount"
    sort_is_artist_albumcount = (is_artists or is_album_artists) and sort == "albumcount"
    sort_is_artist_name = (is_artists or is_album_artists) and sort == "name"

    lambda_sort = lambda x: getattr(x, sort)
    lambda_sort_casefold = lambda x: getattr(x, sort).casefold()

    # Special handling for different sort types
    if sort_is_artist:
        lambda_sort = lambda x: getattr(x, sort)[0]["name"].casefold()
    elif sort_is_artist_name:
        # Use article-aware sorting for artist names
        lambda_sort = lambda x: get_sort_key(getattr(x, sort))
        lambda_sort_casefold = lambda_sort  # Already handles casefolding

    # Apply sorting
    try:
        if sort_is_artist_name:
            # Use the article-aware sorting function
            sorted_items = sorted(items, key=lambda_sort, reverse=reverse)
        else:
            sorted_items = sorted(items, key=lambda_sort_casefold, reverse=reverse)
    except AttributeError:
        sorted_items = sorted(items, key=lambda_sort, reverse=reverse)

    items = sorted_items[start : start + limit]
    album_list = []

    for item in items:
        item_dict = serialize_album(item) if is_albums else serialize_artist(item)

        if is_albums:
            item_dict["help_text"] = f"{item.trackcount} track{'' if item.trackcount == 1 else 's'}"
            item_dict["time"] = timestamp_to_time_passed(item.created_date)
        else:  # artists or album artists
            tracks_text = f"{item.trackcount} track{'' if item.trackcount == 1 else 's'}"
            albums_text = f"{item.albumcount} album{'' if item.albumcount == 1 else 's'}"
            item_dict["help_text"] = f"{albums_text} • {tracks_text}"
            item_dict["time"] = timestamp_to_time_passed(item.created_date)

        album_list.append(item_dict)

    # Calculate pagination info
    has_more = (start + limit) < total
    next_start = start + limit if has_more else None

    return {
        "items": album_list,
        "total": total,
        "start": start,
        "limit": limit,
        "has_more": has_more,
        "next_start": next_start,
    }


@api.get("/stats")
def get_library_stats():
    """
    Get library statistics
    
    Returns counts for albums, artists, album artists, and tracks
    """
    albums = AlbumStore.get_flat_list()
    artists = ArtistStore.get_flat_list()  
    album_artists = AlbumArtistStore.get_flat_list()
    
    # Calculate total tracks
    total_tracks = sum(album.trackcount for album in albums)
    total_duration = sum(getattr(album, 'duration', 0) for album in albums)
    
    return {
        "albums": len(albums),
        "artists": len(artists),
        "album_artists": len(album_artists),
        "tracks": total_tracks,
        "total_duration": total_duration,
        "duration_formatted": seconds_to_time_string(total_duration) if total_duration else "0:00"
    }