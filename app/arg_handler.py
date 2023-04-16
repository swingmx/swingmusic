"""
Handles arguments passed to the program.
"""
import os.path
import sys

from configparser import ConfigParser
import PyInstaller.__main__ as bundler

from app import settings
from app.print_help import HELP_MESSAGE
from app.utils.wintools import is_windows
from app.logger import log
from app.utils.xdg_utils import get_xdg_config_dir

# from app.api.imgserver import set_app_dir

config = ConfigParser()
config.read("pyinstaller.config.ini")

ALLARGS = settings.ALLARGS
ARGS = sys.argv[1:]


class HandleArgs:
    def __init__(self) -> None:
        self.handle_build()
        self.handle_host()
        self.handle_port()
        self.handle_config_path()
        self.handle_no_feat()
        self.handle_remove_prod()
        self.handle_help()
        self.handle_version()

    @staticmethod
    def handle_build():
        """
        Runs Pyinstaller.
        """
        if ALLARGS.build in ARGS:
            with open("pyinstaller.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "True"
                config.write(file)

            _s = ";" if is_windows() else ":"

            bundler.run(
                [
                    "manage.py",
                    "--onefile",
                    "--name",
                    "swingmusic",
                    "--clean",
                    f"--add-data=assets{_s}assets",
                    f"--add-data=client{_s}client",
                    f"--add-data=pyinstaller.config.ini{_s}.",
                    "-y",
                ]
            )

            with open("pyinstaller.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "False"
                config.write(file)

            sys.exit(0)

    @staticmethod
    def handle_port():
        if ALLARGS.port in ARGS:
            index = ARGS.index(ALLARGS.port)
            try:
                port = ARGS[index + 1]
            except IndexError:
                print("ERROR: Port not specified")
                sys.exit(0)

            try:
                settings.FLASKVARS.FLASK_PORT = int(port)  # type: ignore
            except ValueError:
                print("ERROR: Port should be a number")
                sys.exit(0)

    @staticmethod
    def handle_host():
        if ALLARGS.host in ARGS:
            index = ARGS.index(ALLARGS.host)

            try:
                host = ARGS[index + 1]
            except IndexError:
                print("ERROR: Host not specified")
                sys.exit(0)

            settings.FLASKVARS.FLASK_HOST = host  # type: ignore

    @staticmethod
    def handle_config_path():
        """
        Modifies the config path.
        """
        if ALLARGS.config in ARGS:
            index = ARGS.index(ALLARGS.config)

            try:
                config_path = ARGS[index + 1]

                if os.path.exists(config_path):
                    settings.Paths.set_config_dir(config_path)
                    return

                log.warn(f"Config path {config_path} doesn't exist")
                sys.exit(0)
            except IndexError:
                pass

        settings.Paths.set_config_dir(get_xdg_config_dir())

    @staticmethod
    def handle_no_feat():
        # if ArgsEnum.no_feat in ARGS:
        if any((a in ARGS for a in ALLARGS.show_feat)):
            settings.FromFlags.EXTRACT_FEAT = False

    @staticmethod
    def handle_remove_prod():
        if any((a in ARGS for a in ALLARGS.show_prod)):
            settings.FromFlags.REMOVE_PROD = False

    @staticmethod
    def handle_help():
        if any((a in ARGS for a in ALLARGS.help)):
            print(HELP_MESSAGE)
            sys.exit(0)

    @staticmethod
    def handle_version():
        if any((a in ARGS for a in ALLARGS.version)):
            print(settings.Release.APP_VERSION)
            sys.exit(0)
