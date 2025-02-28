##

The Docker container for this release is available here:

https://github.com/orgs/swingmx/packages/container/swingmusic/329450410?tag=v2.0.0.beta10

Get the Android client APK here: https://github.com/swingmx/android/releases

Join our community on Telegram: https://t.me/+9n61PFcgKhozZDE0

## What's new?

Here are the new features, improvements and bug fixes since `v1.4.8`:

1. Authentication and multi-user system

> [!IMPORTANT]
> The default password for the admin account is `admin`. Please change it after logging in.

2. Mixes generated based on your listening activity (experimental, only works with libraries with similar music)
3. Last.fm integration
4. Defaulting to alternate layout on the web client
5. A pairing mechanism for use with the Android client
6. Listening statistics:
   - Charts data showing your top 10 albums, artists and track over periods of the last week, month, or year
   - Various data and play statistics in albums and artists, at the bottom of the page
7. More homepage items:
   - Mixes for you
   - Artist mixes
   - Because you listened to artist (album recommendations)
   - Artists you might like
   - Top artists this week (shown at the end of the week)
   - Top artists this month (shown at the middle and end of the month)
8. Collections: Group together albums/artists like a playlist. Collections are shown in the homepage.
9. Native arm64 builds
10. Use folder images for tracks without embedded album art
11. Tracks with an explicit tag now show an `E` label next to the track title
12. You can prevent artist names from being split by manually editing the `settings.json` file in the config directory
13. You can now use an inline favorite icon by enabling it on the settings
13. More undocumented features, improvements and bug fixes

## Bug fixes

1. Background playback on mobile browsers thanks to @Type-Delta via swingmx/webclient#38
1. Fix: playback issue when track is ~30 seconds to end
1. More undocumented features, improvements and bug fixes

## New Contributors

Shout out to the following people who made various contributions towards this release:

- @Ericgacoki (Android client 🔥🎊)
- @Simonh2o (Web client)
- @jensgrunzer1 (automated Arm64 builds)
- @Type-Delta (Web client)
- @skilletfun (Web client)

> [!WARNING]
> Starting `v2.0.0` (this release) releases are not compatible with older releases. If you point this releases to the config directory of `v14.8`, you will loose all your playlists and favorites.
>
> Please set up this release in a separate config folder if you want to keep your old data . You can do so by passing the `--config <folder>` flag. eg. `./swingmusic --config ~/temp`.

Have fun guys!
