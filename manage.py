"""
This file is used to run the application.
"""
import logging
import os
import sys
from configparser import ConfigParser

import PyInstaller.__main__ as bundler

from app import settings
from app.api import create_api
from app.functions import run_periodic_checks
from app.lib.watchdogg import Watcher as WatchDog
from app.settings import APP_VERSION
from app.settings import HELP_MESSAGE
from app.settings import TCOLOR
from app.setup import run_setup
from app.utils import background
from app.utils import get_home_res_path
from app.utils import get_ip
from app.utils import is_windows

werkzeug = logging.getLogger("werkzeug")
werkzeug.setLevel(logging.ERROR)


class Variables:
    FLASK_PORT = 1970
    FLASK_HOST = "localhost"


app = create_api()
app.static_folder = get_home_res_path("client")

config = ConfigParser()
config.read("pyinstaller.config.ini")


@app.route("/<path:path>")
def serve_client_files(path):
    """
    Serves the static files in the client folder.
    """
    return app.send_static_file(path)


@app.route("/")
def serve_client():
    """
    Serves the index.html file at client/index.html.
    """
    return app.send_static_file("index.html")


ARGS = sys.argv[1:]


class ArgsEnum:
    """
    Enumerates the possible file arguments.
    """

    build = "--build"
    port = "--port"
    host = "--host"
    no_feat = "--no-feat"
    help = ["--help", "-h"]
    version = ["--version", "-v"]


class HandleArgs:

    def __init__(self) -> None:
        self.handle_build()
        self.handle_host()
        self.handle_port()
        self.handle_no_feat()
        self.handle_help()
        self.handle_version()

    @staticmethod
    def handle_build():
        """
        Runs Pyinstaller.
        """
        if ArgsEnum.build in ARGS:
            with open("pyinstaller.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "True"
                config.write(file)

            _s = ";" if is_windows() else ":"

            bundler.run([
                "manage.py",
                "--onefile",
                "--name",
                "swingmusic",
                "--clean",
                f"--add-data=assets{_s}assets",
                f"--add-data=client{_s}client",
                f"--add-data=pyinstaller.config.ini{_s}.",
                "-y",
            ])

            with open("pyinstaller.config.ini", "w", encoding="utf-8") as file:
                config["DEFAULT"]["BUILD"] = "False"
                config.write(file)

            sys.exit(0)

    @staticmethod
    def handle_port():
        if ArgsEnum.port in ARGS:
            index = ARGS.index(ArgsEnum.port)
            try:
                port = ARGS[index + 1]
            except IndexError:
                print("ERROR: Port not specified")
                sys.exit(0)

            try:
                Variables.FLASK_PORT = int(port)  # type: ignore
            except ValueError:
                print("ERROR: Port should be a number")
                sys.exit(0)

    @staticmethod
    def handle_host():
        if ArgsEnum.host in ARGS:
            index = ARGS.index(ArgsEnum.host)

            try:
                host = ARGS[index + 1]
            except IndexError:
                print("ERROR: Host not specified")
                sys.exit(0)

            Variables.FLASK_HOST = host  # type: ignore

    @staticmethod
    def handle_no_feat():
        if ArgsEnum.no_feat in ARGS:
            settings.EXTRACT_FEAT = False

    @staticmethod
    def handle_help():
        if any((a in ARGS for a in ArgsEnum.help)):
            print(HELP_MESSAGE)
            sys.exit(0)

    @staticmethod
    def handle_version():
        if any((a in ARGS for a in ArgsEnum.version)):
            print(APP_VERSION)
            sys.exit(0)


@background
def run_bg_checks() -> None:
    run_setup()
    run_periodic_checks()


@background
def start_watchdog():
    WatchDog().run()


def log_startup_info():
    lines = "---------------------------------------"
    # clears terminal 👇
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")
    # TODO: Check whether the line above breaks Windows terminal's CTRL D

    print(lines)
    print(f"{TCOLOR.HEADER}{APP_VERSION} {TCOLOR.ENDC}")

    if not settings.EXTRACT_FEAT:
        print(
            f"{TCOLOR.OKBLUE}Extracting featured artists from track titles: {TCOLOR.FAIL}DISABLED!{TCOLOR.ENDC}"
        )

    adresses = [Variables.FLASK_HOST]

    if Variables.FLASK_HOST == "0.0.0.0":
        adresses = ["localhost", get_ip()]

    for address in adresses:
        # noinspection HttpUrlsUsage
        print(
            f"Started app on: {TCOLOR.OKGREEN}http://{address}:{Variables.FLASK_PORT}{TCOLOR.ENDC}"
        )

    print(lines)
    print("\n")


if __name__ == "__main__":
    HandleArgs()
    log_startup_info()
    run_bg_checks()
    start_watchdog()

    app.run(
        debug=False,
        threaded=True,
        host=Variables.FLASK_HOST,
        port=Variables.FLASK_PORT,
        use_reloader=False,
    )

# TODO: Find a way to verify the host string
# TODO: Organize code in this file: move args to new file, etc.
