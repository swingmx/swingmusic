from app.settings import ALLARGS, Info
from tabulate import tabulate

args = ALLARGS

help_args_list = [
    ["--help", "-h", "Show this help message"],
    ["--version", "-v", "Show the app version"],
    ["--host", "", "Set the host"],
    ["--port", "", "Set the port"],
    ["--config", "", "Set the config path"],
    ["--no-periodic-scan", "-nps", "Disable periodic scan"],
    ["--pswd", "", "Recover a password"],
    [
        "--scan-interval",
        "-psi",
        "Set the scan interval in seconds. Default 600s (10 minutes)",
    ],
    [
        "--build",
        "",
        "Build the application (in development)",
    ],
]

HELP_MESSAGE = f"""
Swing Music v{Info.SWINGMUSIC_APP_VERSION}

A beautiful, self-hosted music player for your local audio files.
Like Spotify ... but bring your own music.

Usage: ./swingmusic [options] [args]

{tabulate(help_args_list, headers=["Option", "Alias", "Description"], tablefmt="psql", maxcolwidths=[None, None, 40])}
"""
