import os

from app.settings import FLASKVARS, TCOLOR, Keys, Paths
from app.utils.network import get_ip


def log_startup_info():
    lines = "------------------------------"
    # clears terminal 👇
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")

    print(lines)
    print(f"{TCOLOR.HEADER}SwingMusic {Keys.SWINGMUSIC_APP_VERSION} {TCOLOR.ENDC}")

    adresses = [FLASKVARS.get_flask_host()]

    if FLASKVARS.get_flask_host() == "0.0.0.0":
        adresses = ["localhost", get_ip()]

    print("Started app on:")
    for address in adresses:
        # noinspection HttpUrlsUsage
        print(
            f"➤ {TCOLOR.OKGREEN}http://{address}:{FLASKVARS.get_flask_port()}{TCOLOR.ENDC}"
        )

    print(lines + "\n")

    print(f"{TCOLOR.YELLOW}Data folder: {Paths.get_app_dir()}{TCOLOR.ENDC}")
