from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from datetime import datetime
from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore

from swingmusic.serializers.album import serialize_for_card as serialize_album
from swingmusic.serializers.artist import serialize_for_card as serialize_artist
from swingmusic.utils import format_number
from swingmusic.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
    seconds_to_time_string,
    timestamp_to_time_passed,
)

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
        description="The type of items to return (albums | artists)",
        example="albums",
        default="albums",
    )


@api.get("/<itemtype>")
def get_all_items(path: GetAllItemsPath, query: GetAllItemsQuery):
    """
    Get all items

    Used to show all albums or artists in the library

    Sort keys:
    -
    Both albums and artists: `duration`, `created_date`, `playcount`, `playduration`, `lastplayed`, `trackcount`

    Albums only: `title`, `albumartists`, `date`
    Artists only: `name`, `albumcount`
    """
    is_albums = path.itemtype == "albums"
    is_artists = path.itemtype == "artists"

    if is_albums:
        items = AlbumStore.get_flat_list()
    elif is_artists:
        items = ArtistStore.get_flat_list()

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

    sort_is_artist_trackcount = is_artists and sort == "trackcount"
    sort_is_artist_albumcount = is_artists and sort == "albumcount"

    lambda_sort = lambda x: getattr(x, sort)
    lambda_sort_casefold = lambda x: getattr(x, sort).casefold()

    if sort_is_artist:
        lambda_sort = lambda x: getattr(x, sort)[0]["name"].casefold()

    try:
        sorted_items = sorted(items, key=lambda_sort_casefold, reverse=reverse)
    except AttributeError:
        sorted_items = sorted(items, key=lambda_sort, reverse=reverse)

    items = sorted_items[start : start + limit]
    album_list = []

    for item in items:
        item_dict = serialize_album(item) if is_albums else serialize_artist(item)

        if sort_is_date:
            item_dict["help_text"] = datetime.fromtimestamp(item.date).year

        if sort_is_create_date:
            date = create_new_date(datetime.fromtimestamp(item.created_date))
            timeago = date_string_to_time_passed(date)
            item_dict["help_text"] = timeago

        if sort_is_count:
            item_dict["help_text"] = (
                f"{format_number(item.trackcount)} track{'' if item.trackcount == 1 else 's'}"
            )

        if sort_is_duration:
            item_dict["help_text"] = seconds_to_time_string(item.duration)

        if sort_is_artist_trackcount:
            item_dict["help_text"] = (
                f"{format_number(item.trackcount)} track{'' if item.trackcount == 1 else 's'}"
            )

        if sort_is_artist_albumcount:
            item_dict["help_text"] = (
                f"{format_number(item.albumcount)} album{'' if item.albumcount == 1 else 's'}"
            )

        if sort_is_playcount:
            item_dict["help_text"] = (
                f"{format_number(item.playcount)} play{'' if item.playcount == 1 else 's'}"
            )

        if sort_is_lastplayed:
            if item.playduration == 0:
                item_dict["help_text"] = "Never played"
            else:
                item_dict["help_text"] = timestamp_to_time_passed(item.lastplayed)

        if sort_is_playduration:
            item_dict["help_text"] = seconds_to_time_string(item.playduration)

        album_list.append(item_dict)

    return {"items": album_list, "total": total}
