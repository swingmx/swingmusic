# TODO
- Migrations:
    1. Move userdata to new hashing algorithm

- Package jsoni and publish on PyPi
- Rewrite stores to use dictionaries instead of list pools
- last updated date on tracks added via watchdog is broken
- Disable the watchdog by default, and mark it as experimental
- rename userid to server id in config file
- Look into seeding jwts using user password + server id

# DONE
- Support auth headers
- Add recently played playlist
- Move user track logs to user zero
- Move future logs to appropriate user id
- Store (and read) from the correct user account:
    1. Playlists
    2. Favorites