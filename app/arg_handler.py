"""
Handles arguments passed to the program.
"""
import os.path
import sys
from configparser import ConfigParser

import PyInstaller.__main__ as bundler

from app import settings
from app.logger import log
from app.print_help import HELP_MESSAGE
from app.utils.wintools import is_windows
from app.utils.xdg_utils import get_xdg_config_dir

config = ConfigParser()
config.read("runtime.config.ini")

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
        # get last.fm api key from env
        last_fm_key = settings.Keys.LASTFM_API

        # if the key is not in env, exit
        if not last_fm_key:
            log.error("ERROR: LASTFM_API_KEY not set in environment")
            sys.exit(0)

        if ALLARGS.build in ARGS:
            with open("runtime.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "True"

                # copy the api key to the config file
                config["DEFAULT"]["LASTFM_API_KEY"] = last_fm_key
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
                    f"--add-data=runtime.config.ini{_s}.",
                    f"--icon=assets/logo-fill.ico",
                    "-y",
                ]
            )

            # revert build to False and remove the api key for dev mode
            with open("runtime.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "False"
                config["DEFAULT"]["LASTFM_API_KEY"] = ""
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
            print(settings.Release.APP_VERSION)
            sys.exit(0)
