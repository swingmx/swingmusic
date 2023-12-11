"""
Handles arguments passed to the program.
"""
import os.path
import sys

import PyInstaller.__main__ as bundler

from app import settings
from app.logger import log
from app.print_help import HELP_MESSAGE
from app.utils.xdg_utils import get_xdg_config_dir
from app.utils.wintools import is_windows

ALLARGS = settings.ALLARGS
ARGS = sys.argv[1:]


class HandleArgs:
    def __init__(self) -> None:
        self.handle_build()
        self.handle_host()
        self.handle_port()
        self.handle_config_path()

        self.handle_periodic_scan()
        self.handle_periodic_scan_interval()

        self.handle_help()
        self.handle_version()

    @staticmethod
    def handle_build():
        """
        Runs Pyinstaller.
        """

        if ALLARGS.build not in ARGS:
            return

        if settings.IS_BUILD:
            print("Do the cha cha slide instead!")
            print("https://www.youtube.com/watch?v=wZv62ShoStY")
            sys.exit(0)

        config_keys = [
            "LASTFM_API_KEY",
            "PLUGIN_LYRICS_AUTHORITY",
            "PLUGIN_LYRICS_ROOT_URL",
            "SWINGMUSIC_APP_VERSION",
        ]

        lines = []

        for key in config_keys:
            value = settings.Keys.get(key)

            if not value:
                log.error(f"ERROR: {key} not set in environment")
                sys.exit(0)

            lines.append(f'{key} = "{value}"\n')

        try:
            with open("./app/configs.py", "w", encoding="utf-8") as file:
                # copy the api keys to the config file
                file.writelines(lines)

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
                    f"--icon=assets/logo-fill.light.ico",
                    "-y",
                ]
            )
        finally:
            # revert and remove the api keys for dev mode
            with open("./app/configs.py", "w", encoding="utf-8") as file:
                lines = [f'{key} = ""\n' for key in config_keys]
                file.writelines(lines)

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

            settings.FLASKVARS.set_flask_host(host)  # type: ignore

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
    def handle_periodic_scan():
        if any((a in ARGS for a in ALLARGS.no_periodic_scan)):
            settings.SessionVars.DO_PERIODIC_SCANS = False

    @staticmethod
    def handle_periodic_scan_interval():
        if any((a in ARGS for a in ALLARGS.periodic_scan_interval)):
            index = [
                ARGS.index(a) for a in ALLARGS.periodic_scan_interval if a in ARGS
            ][0]

            try:
                interval = ARGS[index + 1]
            except IndexError:
                print("ERROR: Interval not specified")
                sys.exit(0)

            try:
                psi = int(interval)
            except ValueError:
                print("ERROR: Interval should be a number")
                sys.exit(0)

            if psi < 0:
                print("WADAFUCK ARE YOU TRYING?")
                sys.exit(0)

            settings.SessionVars.PERIODIC_SCAN_INTERVAL = psi

    @staticmethod
    def handle_help():
        if any((a in ARGS for a in ALLARGS.help)):
            print(HELP_MESSAGE)
            sys.exit(0)

    @staticmethod
    def handle_version():
        if any((a in ARGS for a in ALLARGS.version)):
            print(settings.Keys.SWINGMUSIC_APP_VERSION)
            sys.exit(0)
