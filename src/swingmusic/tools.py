"""
Handles arguments passed to the program.
"""
import sys
from getpass import getpass
from swingmusic.db.userdata import UserTable
from swingmusic.setup.sqlite import setup_sqlite
from swingmusic.utils.auth import hash_password


def handle_password_reset():
    """
    Handles the --password-reset argument. Resets the password.
    """

    setup_sqlite()

    # collect username
    try:
        username = input("Enter username: ")
    except KeyboardInterrupt:
        print("\nOperation cancelled! Exiting ...")
        return

    username = username.strip()
    user = UserTable.get_by_username(username)

    if not user:
        print(f"User {username} not found")
        return

    # collect password
    try:
        password = getpass("Enter new password: ")
    except KeyboardInterrupt:
        print("\nOperation cancelled! Exiting ...")
        return

    try:
        UserTable.update_one({"id": user.id, "password": hash_password(password)})
        print("Password reset successfully!")
    except Exception as e:
        print(f"Error resetting password: {e}")
        return
