"""
Handles Tool argument functions
"""

import sys
from getpass import getpass

import click
import PyInstaller.__main__ as bundler

from swingmusic import settings
from swingmusic.db.userdata import UserTable
from swingmusic.logger import log
from swingmusic.setup.sqlite import setup_sqlite
from swingmusic.utils.auth import hash_password
from swingmusic.utils.paths import getFlaskOpenApiPath
from swingmusic.utils.wintools import is_windows

from flask import Response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
)

from datetime import datetime, timezone


def handle_build():
    """
    build swingmusic into single executable
    """

    if settings.IS_BUILD:
        click.echo("Can't build the project. Exiting ...")
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
            log.error(
                f"WARNING: {key} not resolved. Can't build the project. Exiting ..."
            )
            sys.exit(0)

        lines.append(f'{key} = "{value}"\n')

    try:
        # write the info to the config file
        with open("./app/configs.py", "w", encoding="utf-8") as file:
            # copy the api keys to the config file
            file.writelines(lines)

        _s = ";" if is_windows() else ":"

        flask_openapi_path = getFlaskOpenApiPath()
        server_module = "waitress" if is_windows() else "bjoern"

        bundler.run(
            [
                "main.py",
                "--onefile",
                "--name",
                "swingmusic",
                "--clean",
                f"--add-data=assets{_s}assets",
                f"--add-data=client{_s}client",
                f"--add-data=version.txt{_s}.",
                f"--add-data={flask_openapi_path}/templates/static{_s}flask_openapi3/templates/static",
                f"--hidden-import={server_module}",
                "--icon=assets/logo-fill.light.ico",
                "-y",
            ]
        )
    finally:
        # revert and remove the api keys for dev mode
        with open("./app/configs.py", "w", encoding="utf-8") as file:
            lines = [f'{key} = ""\n' for key in info_keys]
            file.writelines(lines)

        sys.exit(0)


def handle_password_reset() -> None:
    """
    Resets the password.
    user will get asked for username and password directly.
    No params needed
    """

    setup_sqlite()

    username: str = ""
    password: str = ""

    # collect username
    try:
        username = input("Enter username: ").strip()
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled! Exiting ...")
        sys.exit(0)

    user = UserTable.get_by_username(username)

    if not user:
        click.echo(f"User {username} not found")
        sys.exit(0)

    # collect password
    try:
        password = getpass("Enter new password: ")
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled! Exiting ...")
        sys.exit(0)

    try:
        UserTable.update_one({"id": user.id, "password": hash_password(password)})
        click.echo("Password reset successfully!")
    except Exception as e:
        click.echo(f"Error resetting password: {e}")
        sys.exit(0)

    sys.exit(0)