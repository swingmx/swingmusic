import os
from swingmusic.settings import TCOLOR, Metadata, Paths
from swingmusic.utils.network import get_ip


def log_startup_info(host: str, port: int):
    pid = os.getpid()
    print(f"{TCOLOR.HEADER}Swing Music v{Metadata.version} (PID: {pid}) {TCOLOR.ENDC}")

    in_docker = os.environ.get("SWINGMUSIC_IN_DOCKER") == "1" or os.path.exists(
        "/.dockerenv"
    )

    addresses = [host]

    if host == "0.0.0.0":
        if in_docker:
            # get_ip() returns the docker bridge address, which isn't reachable from the host.
            addresses.append("127.0.0.1")
        else:
            remote_ip = get_ip()
            addresses.extend(["127.0.0.1"] + ([remote_ip] if remote_ip else []))

    print("Server running on:\n")
    for address in addresses:
        print(f"{TCOLOR.OKGREEN}http://{address}:{port}{TCOLOR.ENDC}")

    print(f"\n{TCOLOR.YELLOW}Data folder: {Paths().config_dir}{TCOLOR.ENDC}\n")
