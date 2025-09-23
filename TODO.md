# @michily TODO

## UI
* Auto update WebUI - version check + api missing
* Web UI - Remove https from index.html for http support?
* Web UI could use continues build like https://github.com/AppImage/AppImageKit/releases/download/continuous/
* Web UI - playlist not shown in folder view
* rework argparse with subparser. Currently not clear what commands allow what args

## Building:
* AppImage build is currently broken view [python-appimage: Issues 95](https://github.com/niess/python-appimage/issues/94) aka I bypassed it.
* Optimise docker/speed build up

## Server:
* Rework song name/autor/.. parsing to only support filetags. Only fall back when user-enabled and manual regex is set. see Telegram
* Publish this on PyPi

## Multithreading
* Multiprocessing creates new paths - sync between processes. <- env is recommended.
* Fix singleton global in multiprocessing - own process, own memory, own sys.modules cache <- env is recommended.

## Auth:
* more multiuser control
* audit log
* one auth method for all e.g. jwt in Header?

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

```
Traceback (most recent call last):
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_openapi3/scaffold.py", line 117, in view_func
    response = func(**func_kwargs)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/api/scrobble/__init__.py", line 86, in log_track
    RecentlyPlayed(userid=scrobble_data["userid"])
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 23, in __init__
    super().__init__()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/__init__.py", line 21, in __init__
    self.run()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 40, in run
    store_entry = HomepageStore.entries[self.store_key].items[
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 1
ERROR:swingmusic.app_builder:Exception on /logger/track/log [POST]
Traceback (most recent call last):
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_openapi3/scaffold.py", line 117, in view_func
    response = func(**func_kwargs)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/api/scrobble/__init__.py", line 86, in log_track
    RecentlyPlayed(userid=scrobble_data["userid"])
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 23, in __init__
    super().__init__()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/__init__.py", line 21, in __init__
    self.run()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 40, in run
    store_entry = HomepageStore.entries[self.store_key].items[
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 1
ERROR:swingmusic.app_builder:Exception on /logger/track/log [POST]
Traceback (most recent call last):
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/.venv/lib/python3.12/site-packages/flask_openapi3/scaffold.py", line 117, in view_func
    response = func(**func_kwargs)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/api/scrobble/__init__.py", line 86, in log_track
    RecentlyPlayed(userid=scrobble_data["userid"])
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 23, in __init__
    super().__init__()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/__init__.py", line 21, in __init__
    self.run()
  File "/Users/cwilvx/code/swingmusic/src/swingmusic/lib/recipes/recents.py", line 40, in run
    store_entry = HomepageStore.entries[self.store_key].items[
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 1
```