from flask_jwt_extended import current_user
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from app.api.apischemas import GenericLimitSchema
from app.lib.home.recentlyadded import get_recently_added_items
from app.lib.home.recentlyplayed import get_recently_played

bp_tag = Tag(name="Home", description="Homepage items")
api = APIBlueprint("home", __name__, url_prefix="/home", abp_tags=[bp_tag])


@api.get("/recents/added")
def get_recently_added(query: GenericLimitSchema):
    """
    Get recently added
    """
    return {"items": get_recently_added_items(query.limit)}


@api.get("/recents/played")
def get_recent_plays(query: GenericLimitSchema):
    """
    Get recently played
    """
    return {"items": get_recently_played(query.limit)}
