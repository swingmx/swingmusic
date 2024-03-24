from flask import Blueprint, request

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from app.db.sqlite.plugins import PluginsMethods

bp_tag = Tag(name="Plugins", description="Manage plugins")
api = APIBlueprint("plugins", __name__, url_prefix="/plugins", abp_tags=[bp_tag])


@api.get("/")
def get_all_plugins():
    """
    List all plugins
    """
    plugins = PluginsMethods.get_all_plugins()

    return {"plugins": plugins}


class PluginBody(BaseModel):
    plugin: str = Field(description="The plugin name", example="lyrics")


class PluginActivateBody(PluginBody):
    active: bool = Field(
        description="New plugin active state", example=False, default=False
    )


@api.post("/setactive")
def activate_deactivate_plugin(body: PluginActivateBody):
    """
    Activate/Deactivate plugin
    """
    name = body.plugin
    active = 1 if body.active else 0

    PluginsMethods.plugin_set_active(name, active)

    return {"message": "OK"}, 200


class PluginSettingsBody(PluginBody):
    settings: dict = Field(
        description="The new plugin settings", example={"key": "value"}
    )


@api.post("/settings")
def update_plugin_settings(body: PluginSettingsBody):
    """
    Update plugin settings
    """
    plugin = body.plugin
    settings = body.settings

    if not plugin or not settings:
        return {"error": "Missing plugin or settings"}, 400

    PluginsMethods.update_plugin_settings(plugin_name=plugin, settings=settings)
    plugin = PluginsMethods.get_plugin_by_name(plugin)

    return {"status": "success", "settings": plugin.settings}
