from app.settings import ALLARGS

args = ALLARGS

HELP_MESSAGE = f"""
Usage: swingmusic [options]

   Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music. 

Options:
    {', '.join(args.help.value)}: Show this help message
    {', '.join(args.version.value)}: Show the app version
    
    {args.host}: Set the host
    {args.port}: Set the port
    {args.config}: Set the config path
    
    {', '.join(args.show_feat.value)}: Do not extract featured artists from the song title
    {', '.join(args.show_prod.value)}: Do not hide producers in the song title
    {', '.join(args.dont_clean_albums.value)}: Don't clean album titles. Cleaning is done by removing information in 
                             parentheses and showing it separately
    {', '.join(args.dont_clean_tracks.value)}: Don't remove remaster information from track titles
    {', '.join(args.no_periodic_scan.value)}: Disable periodic scan
    {', '.join(args.periodic_scan_interval.value)}: Set the periodic scan interval in seconds. Default is 300 seconds (5 
    minutes)
    
    {args.build}: Build the application (in development)
"""
