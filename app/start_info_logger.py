import os

from app.settings import TCOLOR, APP_VERSION, FLASKVARS, APP_DIR
from app import settings
from app.utils.network import get_ip


def log_startup_info():
    lines = "------------------------------"
    # clears terminal 👇
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")

    print(lines)
    print(f"{TCOLOR.HEADER}SwingMusic {APP_VERSION} {TCOLOR.ENDC}")

    adresses = [FLASKVARS.FLASK_HOST]

    if FLASKVARS.FLASK_HOST == "0.0.0.0":
        adresses = ["localhost", get_ip()]

    print("Started app on:")
    for address in adresses:
        # noinspection HttpUrlsUsage
        print(
            f"➤ {TCOLOR.OKGREEN}http://{address}:{FLASKVARS.FLASK_PORT}{TCOLOR.ENDC}"
        )

    print(lines)
    print("\n")

    to_print = [
        [
            "Extract featured artists from titles",
            settings.EXTRACT_FEAT
        ],
        [
            "Remove prod. from titles",
            settings.REMOVE_PROD
        ]
    ]

    for item in to_print:
        print(
            f"{item[0]}: {TCOLOR.FAIL}{item[1]}{TCOLOR.ENDC}"
        )

    print(
        f"{TCOLOR.YELLOW}Data folder: {APP_DIR}{TCOLOR.ENDC}"
    )

    print("\n")
