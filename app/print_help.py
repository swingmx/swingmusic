from app.settings import ALLARGS

args = ALLARGS

HELP_MESSAGE = f"""
Usage: swingmusic [options]

   Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music. 

Options:
    {', '.join(args.help)}: Show this help message
    {', '.join(args.version)}: Show the app version

    {args.host}: Set the host
    {args.port}: Set the port
    {args.config}: Set the config path

    {', '.join(args.no_periodic_scan)}: Disable periodic scan
    {', '.join(args.periodic_scan_interval)}: Set the periodic scan interval in seconds. Default is 300 seconds (5 
    minutes)

    {args.build}: Build the application (in development)
"""
