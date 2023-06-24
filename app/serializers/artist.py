# from dataclasses import asdict


# def album_serializer(album: Artist, to_remove: set[str]) -> ArtistMinimal:
#     album_dict = asdict(album)

#     to_remove.update(key for key in album_dict.keys() if key.startswith("is_"))
#     for key in to_remove:
#         album_dict.pop(key, None)

#     return album_dict


# Traceback (most recent call last):
#   File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
#     self.run()
#   File "/usr/lib/python3.10/threading.py", line 953, in run
#     self._target(*self._args, **self._kwargs)
#   File "/usr/lib/python3.10/multiprocessing/pool.py", line 579, in _handle_results
#     task = get()
#   File "/usr/lib/python3.10/multiprocessing/connection.py", line 251, in recv
#     return _ForkingPickler.loads(buf.getbuffer())
#   File "/home/cwilvx/.cache/pypoetry/virtualenvs/swing_music_player-xIXBgWdk-py3.10/lib/python3.10/site-packages/requests/exceptions.py", line 41, in __init__
#     CompatJSONDecodeError.__init__(self, *args)
# TypeError: JSONDecodeError.__init__() missing 2 required positional arguments: 'doc' and 'pos'
