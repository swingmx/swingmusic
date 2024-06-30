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
- Remove all stores
- Review: We don't need server side image colors
- Clean up main db and userdata modules
- Move plugins to a config file
- What about our migrations?
- Add userid to queries
- Remove duplicates on artist page (test with Hanson)
- Test foreign keys on delete
- Map scrobble info on app start
