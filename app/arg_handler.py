"""
Handles arguments passed to the program.
"""

import sys

from configparser import ConfigParser
import PyInstaller.__main__ as bundler

from app import settings
from app.print_help import HELP_MESSAGE
from app.utils.wintools import is_windows

config = ConfigParser()
config.read("pyinstaller.config.ini")

ALLARGS = settings.ALLARGS
ARGS = sys.argv[1:]


class HandleArgs:
    def __init__(self) -> None:
        self.handle_build()
        self.handle_host()
        self.handle_port()
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
    def handle_no_feat():
        # if ArgsEnum.no_feat in ARGS:
        if any((a in ARGS for a in ALLARGS.show_feat)):
            settings.EXTRACT_FEAT = False

    @staticmethod
    def handle_remove_prod():
        if any((a in ARGS for a in ALLARGS.show_prod)):
            settings.REMOVE_PROD = False

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
