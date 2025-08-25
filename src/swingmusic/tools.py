"""
All tools ``swingmusic`` provide without UI
"""

from getpass import getpass
from swingmusic.db.userdata import UserTable
from swingmusic.setup.sqlite import setup_sqlite
from swingmusic.utils.auth import hash_password
from swingmusic.settings import Paths
from pathlib import Path
from PIL import Image

def handle_password_reset(base_path:Path|None):
    """
    Handles the --password-reset argument. Resets the password.
    """

    Paths(base_path.resolve(), None)

    setup_sqlite()

    # collect username
    try:
        username = input("Enter username: ")
        username = username.strip()
        user = UserTable.get_by_username(username)

        if not user:
            print(f"User {username} not found")
            return

        password = getpass("Enter new password: ")

    except KeyboardInterrupt:
        print("\nOperation cancelled! Exiting ...")
        return

    try:
        UserTable.update_one({"id": user.id, "password": hash_password(password)})
        print("Password reset successfully!")
    except Exception as e:
        print(f"Error resetting password: {e}")


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    padding = 7
    icon_path = Paths().assets_path / "logo-fill.light.ico"
    image = Image.open(icon_path)

    # Calculate new size with padding
    new_size = (width - 2 * padding, height - 2 * padding)

    # Resize the image while maintaining aspect ratio
    image.thumbnail(new_size, Image.Resampling.LANCZOS)

    # Create a new image with padding
    padded_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Calculate position to center the image
    x = (width - image.width) // 2
    y = (height - image.height) // 2

    # Paste the resized image onto the padded image
    padded_image.paste(image, (x, y), image)

    return padded_image