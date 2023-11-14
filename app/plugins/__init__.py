class Plugin:
    """
    Class that all plugins should inherit from
    """

    def __init__(self, name: str, description: str) -> None:
        self.enabled = False
        self.name = name
        self.description = description

    def set_active(self, state: bool):
        self.enabled = state


def plugin_method(func):
    """
    A decorator that prevents execution if the plugin is disabled.
    Should be used on all plugin methods
    """

    def wrapper(*args, **kwargs):
        plugin: Plugin = args[0]

        if plugin.enabled:
            return func(*args, **kwargs)
        else:
            return

    return wrapper

