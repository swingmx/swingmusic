from app.settings import ALLARGS

args = ALLARGS

HELP_MESSAGE = f"""
Usage: swingmusic [options]

Options:
    {args.build}: Build the application (in development)
    {args.host}: Set the host
    {args.port}: Set the port

    {', '.join(args.show_feat)}: Do not extract featured artists from the song title
    {', '.join(args.show_prod)}: Do not hide producers in the song title

    {', '.join(args.help)}: Show this help message
    {', '.join(args.version)}: Show the app version
"""
