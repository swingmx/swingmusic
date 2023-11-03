from flask import Blueprint, request

from app.db.sqlite.plugins import PluginsMethods


api = Blueprint("plugins", __name__, url_prefix="/plugins")


@api.route("/", methods=["GET"])
def get_all_plugins():
    plugins = PluginsMethods.get_all_plugins()

    return {"plugins": plugins}


@api.route("/setactive", methods=["GET"])
def activate_deactivate_plugin():
    name = request.args.get("plugin", None)
    state = request.args.get("state", None)

    if not name or not state:
        return {"error": "Missing plugin or state"}, 400

    PluginsMethods.plugin_set_active(name, int(state))

    return {"message": "OK"}, 200
