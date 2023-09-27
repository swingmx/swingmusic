from app.settings import ALLARGS
from tabulate import tabulate

args = ALLARGS

help_args_list = [
    ["--help", "-h", "Show this help message"],
    ["--version", "-v", "Show the app version"],
    ["--host", "", "Set the host"],
    ["--port", "", "Set the port"],
    ["--config", "", "Set the config path"],
    ["--no-periodic-scan", "-nps", "Disable periodic scan"],
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
Swing Music is a beautiful, self-hosted music player for your 
local audio files. Like a cooler Spotify ... but bring your own music.

Usage: swingmusic [options] [args]

{tabulate(help_args_list, headers=["Option", "Short", "Description"], tablefmt="simple_grid", maxcolwidths=[None, None, 40])}
"""
