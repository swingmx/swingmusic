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
        self.handle_cleaning_albums()
        self.handle_cleaning_tracks()
        self.handle_periodic_scan()
        self.handle_periodic_scan_interval()

        self.handle_help()
        self.handle_version()

    @staticmethod
    def handle_build():
        """
        Runs Pyinstaller.
        """
        if ALLARGS.build.value in ARGS:
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
        if ALLARGS.port.value in ARGS:
            index = ARGS.index(ALLARGS.port.value)
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
        if ALLARGS.host.value in ARGS:
            index = ARGS.index(ALLARGS.host.value)

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
        if ALLARGS.config.value in ARGS:
            index = ARGS.index(ALLARGS.config.value)

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
        if any((a in ARGS for a in ALLARGS.show_feat.value)):
            settings.FromFlags.EXTRACT_FEAT = False

    @staticmethod
    def handle_remove_prod():
        if any((a in ARGS for a in ALLARGS.show_prod.value)):
            settings.FromFlags.REMOVE_PROD = False

    @staticmethod
    def handle_cleaning_albums():
        if any((a in ARGS for a in ALLARGS.dont_clean_albums.value)):
            settings.FromFlags.CLEAN_ALBUM_TITLE = False

    @staticmethod
    def handle_cleaning_tracks():
        if any((a in ARGS for a in ALLARGS.dont_clean_tracks.value)):
            settings.FromFlags.REMOVE_REMASTER_FROM_TRACK = False

    @staticmethod
    def handle_periodic_scan():
        if any((a in ARGS for a in ALLARGS.no_periodic_scan.value)):
            settings.FromFlags.DO_PERIODIC_SCANS = False

    @staticmethod
    def handle_periodic_scan_interval():
        if any((a in ARGS for a in ALLARGS.periodic_scan_interval.value)):
            index = [ARGS.index(a) for a in ALLARGS.periodic_scan_interval.value if a in ARGS][0]

            try:
                interval = ARGS[index + 1]
            except IndexError:
                print("ERROR: Interval not specified")
                sys.exit(0)

            # psi = 0

            try:
                psi = int(interval)
            except ValueError:
                print("ERROR: Interval should be a number")
                sys.exit(0)

            if psi < 0:
                print("WADAFUCK ARE YOU TRYING?")
                sys.exit(0)

            settings.FromFlags.PERIODIC_SCAN_INTERVAL = psi

    @staticmethod
    def handle_help():
        if any((a in ARGS for a in ALLARGS.help.value)):
            print(HELP_MESSAGE)
            sys.exit(0)

    @staticmethod
    def handle_version():
        if any((a in ARGS for a in ALLARGS.version.value)):
            print(settings.Release.APP_VERSION)
            sys.exit(0)
