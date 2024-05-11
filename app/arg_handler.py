"""
Handles arguments passed to the program.
"""

from getpass import getpass
import os.path
import sys

import PyInstaller.__main__ as bundler

from app import settings
from app.logger import log
from app.print_help import HELP_MESSAGE
from app.utils.auth import hash_password
from app.utils.paths import getFlaskOpenApiPath
from app.utils.xdg_utils import get_xdg_config_dir
from app.utils.wintools import is_windows
from app.db.sqlite.auth import SQLiteAuthMethods as authdb

ALLARGS = settings.ALLARGS
ARGS = sys.argv[1:]


class ProcessArgs:
    """
    Processes the arguments passed to the program.
    """

    def __init__(self) -> None:
        # resolve config path
        self.handle_config_path()  # 1

        # handles that exit
        self.handle_password_recovery()
        self.handle_build()
        self.handle_help()
        self.handle_version()

        # non-exiting handles
        self.handle_host()
        self.handle_port()
        self.handle_periodic_scan()
        self.handle_periodic_scan_interval()

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

        info_keys = [
            "SWINGMUSIC_APP_VERSION",
            "GIT_LATEST_COMMIT_HASH",
            "GIT_CURRENT_BRANCH",
        ]

        lines = []

        for key in info_keys:
            value = settings.Info.get(key)

            if not value:
                log.error(f"WARNING: {key} not resolved. Exiting ...")
                sys.exit(0)

            lines.append(f'{key} = "{value}"\n')

        try:
            # write the info to the config file
            with open("./app/configs.py", "w", encoding="utf-8") as file:
                # copy the api keys to the config file
                file.writelines(lines)

            _s = ";" if is_windows() else ":"

            flask_openapi_path = getFlaskOpenApiPath()

            bundler.run(
                [
                    "manage.py",
                    "--onefile",
                    "--name",
                    "swingmusic",
                    "--clean",
                    f"--add-data=assets{_s}assets",
                    f"--add-data=client{_s}client",
                    f"--add-data={flask_openapi_path}/templates/static{_s}flask_openapi3/templates/static",
                    f"--icon=assets/logo-fill.light.ico",
                    "-y",
                ]
            )
        finally:
            # revert and remove the api keys for dev mode
            with open("./app/configs.py", "w", encoding="utf-8") as file:
                lines = [f'{key} = ""\n' for key in info_keys]
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
                resolved = os.path.abspath(config_path)

                if os.path.exists(resolved):
                    settings.Paths.set_config_dir(resolved)
                    return

                log.warn(f"Config path {resolved} doesn't exist")
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
            print(f"VERSION: v{settings.Info.SWINGMUSIC_APP_VERSION}")
            print(
                f"COMMIT#: {settings.Info.GIT_CURRENT_BRANCH}/{settings.Info.GIT_LATEST_COMMIT_HASH}"
            )
            sys.exit(0)

    @staticmethod
    def handle_password_recovery():
        if ALLARGS.pswd in ARGS:
            print("SWING MUSIC v2.0.0 ")
            print("PASSWORD RECOVERY \n")

            username: str = ""
            password: str = ""

            # collect username
            try:
                username = input("Enter username: ")
            except KeyboardInterrupt:
                print("\nOperation cancelled! Exiting ...")
                sys.exit(0)

            username = username.strip()
            user = authdb.get_user_by_username(username)

            if not user:
                print(f"User {username} not found")
                sys.exit(0)

            # collect password
            try:
                password = getpass("Enter new password: ")
            except KeyboardInterrupt:
                print("\nOperation cancelled! Exiting ...")
                sys.exit(0)

            password = hash_password(password)
            user = authdb.update_user({"id": user.id, "password": password})

            sys.exit(0)
