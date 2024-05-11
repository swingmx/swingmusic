from flask import Blueprint

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from datetime import datetime
from app.api.apischemas import GenericLimitSchema
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore

from app.serializers.album import serialize_for_card as serialize_album
from app.serializers.artist import serialize_for_card as serialize_artist
from app.utils import format_number
from app.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
    seconds_to_time_string,
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
    """
    is_albums = path.itemtype == "albums"
    is_artists = path.itemtype == "artists"

    items = AlbumStore.albums

    if is_artists:
        items = ArtistStore.artists

    start = query.start
    limit = query.limit
    sort = query.sortby
    reverse = query.reverse == "1"

    sort_is_count = sort == "count"
    sort_is_duration = sort == "duration"
    sort_is_create_date = sort == "created_date"

    sort_is_date = is_albums and sort == "date"
    sort_is_artist = is_albums and sort == "albumartists"

    sort_is_artist_trackcount = is_artists and sort == "trackcount"
    sort_is_artist_albumcount = is_artists and sort == "albumcount"

    lambda_sort = lambda x: getattr(x, sort)
    if sort_is_artist:
        lambda_sort = lambda x: getattr(x, sort)[0].name

    sorted_items = sorted(items, key=lambda_sort, reverse=reverse)
    items = sorted_items[start : start + limit]

    album_list = []

    for item in items:
        item_dict = serialize_album(item) if is_albums else serialize_artist(item)

        if sort_is_date:
            item_dict["help_text"] = item.date

        if sort_is_create_date:
            date = create_new_date(datetime.fromtimestamp(item.created_date))
            timeago = date_string_to_time_passed(date)
            item_dict["help_text"] = timeago

        if sort_is_count:
            item_dict["help_text"] = (
                f"{format_number(item.count)} track{'' if item.count == 1 else 's'}"
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

        album_list.append(item_dict)

    return {"items": album_list, "total": len(sorted_items)}
