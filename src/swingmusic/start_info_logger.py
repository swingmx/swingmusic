from swingmusic.settings import TCOLOR, Info, Paths
from swingmusic.utils.network import get_ip
import click


def log_startup_info(host: str, port: int):
    lines = "-"*30
    # clears terminal 👇
    # os.system("cls" if os.name == "nt" else "echo -e \\\\033c")

    click.echo(f"{TCOLOR.HEADER}Swing Music v{Info.SWINGMUSIC_APP_VERSION} {TCOLOR.ENDC}")

    addresses = [host]

    if host == "0.0.0.0":
        remote_ip = get_ip()
        addresses.extend(["127.0.0.1"] + ([remote_ip] if remote_ip else []))

    click.echo("Server running on:\n")
    for address in addresses:
        click.echo(
            f"{TCOLOR.OKGREEN}http://{address}:{port}{TCOLOR.ENDC}"
        )

    click.echo("")
    click.echo(f"{TCOLOR.YELLOW}Data folder: {Paths.get_app_dir()}{TCOLOR.ENDC}\n")
