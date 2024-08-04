# TODO

- Migrations:

  1. Move userdata to new hashing algorithm
     - favorites ✅
     - playlists
     - scrobble
     - images
     - remove image colors

- Package jsoni and publish on PyPi
- Rewrite stores to use dictionaries instead of list pools
- last updated date on tracks added via watchdog is broken
- Disable the watchdog by default, and mark it as experimental
- rename userid to server id in config file
- Look into seeding jwts using user password + server id
- Recreate album hash if featured artists are discover
- Implement checking if is clean install and skip migrations!

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

- Updating settings
- Cleaning out commented code
- Watchdog
- Periodic scans
- Remove legacy db methods
- Review: We don't need server side image colors
- Clean up main db and userdata modules
- Move plugins to a config file
- What about our migrations?
- Add userid to queries
- Remove duplicates on artist page (test with Hanson)
- Test foreign keys on delete
- Normalize playlists table:
  - New table to hold playlist entries
- Normalize similar artists:
  - New table to hold similar artist entries
  - Create 2 way relationships, such that if an artist A is similar to another B with a certain weight,
    then artist B is similar to A with the same weight, unless overwritten.

# Bug fixes

- Duplicates on search
- Audio stops on ending
- Port account settings to config on the frontend