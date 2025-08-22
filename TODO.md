# TMP


## UI
* Auto update WebUI
* UI - Remove https from index.html for http support
* UI should resolve into config dir <- for auto update -> update all build files with this change
* UI could use continues build like https://github.com/AppImage/AppImageKit/releases/download/continuous/

* AppImage build is currently broken view [python-appimage: Issues 95](https://github.com/niess/python-appimage/issues/94)

* Assets should either move to UI or inside the project. Importlib cannot securely resolve this path if it is not inside the src dir.
* arm builds
* Rework parsing to only support tags and fall back only when enabled and set to parsing with name/path. see Telegram
* Publish this on PyPi

* Multiprocessing creates new paths - sync between processes.
* Fix singleton global in multiprocessing - own process, own memory, own sys.modules cache

# TODO

- Migrations:

  1. Move userdata to new hashing algorithm
     - favorites ✅
     - playlists
     - scrobble
     - images
     - remove image colors

- Package jsoni and publish on PyPi
- last updated date on tracks added via watchdog is broken
- Disable the watchdog by default, and mark it as experimental
- rename userid to server id in config file
- Look into seeding jwts using user password + server id


<!-- CHECKPOINT -->
<!-- ALBUM PAGE! -->

# DONE

- Support auth headers
- Add recently played playlist
- Move user track logs to user zero
- Move future logs to appropriate user id
- Store (and read) from the correct user account:
  1. Playlists
  2. Favorites

# THE BIG ONE

- Watchdog
- Periodic scans
- What about our migrations?
- Test foreign keys on delete
- Normalize playlists table:
  - New table to hold playlist entries
- Normalize similar artists:
  - New table to hold similar artist entries
  - Create 2 way relationships, such that if an artist A is similar to another B with a certain weight,
    then artist B is similar to A with the same weight, unless overwritten.
- Clean up tempfiles after transcoding
- Double sort artist tracks for consistency (alphabetically then by other field. eg. playcount)

# Bug fixes

- Duplicates on search
- Audio stops on ending
- Show users on account settings when logged in as admin and show users on login is disabled.
- Save both filepath and trackhash in favorites and playlists
