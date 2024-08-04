from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from app.api.auth import admin_required
from app.db.userdata import PluginTable

bp_tag = Tag(name="Plugins", description="Manage plugins")
api = APIBlueprint("plugins", __name__, url_prefix="/plugins", abp_tags=[bp_tag])


@api.get("/")
def get_all_plugins():
    """
    List all plugins
    """
    plugins = PluginTable.get_all()
    return {"plugins": plugins}


class PluginBody(BaseModel):
    plugin: str = Field(description="The plugin name", example="lyrics")


class PluginActivateBody(PluginBody):
    active: bool = Field(
        description="New plugin active state", example=False, default=False
    )


@api.post("/setactive")
@admin_required()
def activate_deactivate_plugin(body: PluginActivateBody):
    """
    Activate/Deactivate plugin
    """
    name = body.plugin
    PluginTable.activate(name, body.active)

    return {"message": "OK"}, 200


class PluginSettingsBody(PluginBody):
    settings: dict = Field(
        description="The new plugin settings", example={"key": "value"}
    )


@api.post("/settings")
@admin_required()
def update_plugin_settings(body: PluginSettingsBody):
    """
    Update plugin settings
    """
    plugin = body.plugin
    settings = body.settings

    if not plugin or not settings:
        return {"error": "Missing plugin or settings"}, 400

    PluginTable.update_settings(plugin, settings)
    plugin = PluginTable.get_by_name(plugin)

    return {"status": "success", "settings": plugin.settings}
