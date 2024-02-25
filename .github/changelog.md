# What's New?

- New alternative (no sidebar) layout
- Added search bar on the top bar
- Automatic preloading of next track, meaning reduced delay between tracks. Impact most noticable on reverse proxy.
- Quick actions in settings page
- Toggle right sidebar using CTRL + B
- Move to a stronger WSGI server ([waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/))
- Proper ARM64 and other platforms support
- A Proper timezone fix. Thanks to @tcsenpai on #170
- Hovering over a recently played/added item on the homepage will reveal how long ago
- Recently added items will not have a cutoff
- The exhaustive list of web client stuff can be found on [commit 4211ccc](https://github.com/swing-opensource/swingmusic-client/commit/4211ccc685e3d33dbf008cbb6c77542baf0130dc) in the client repo.

# Bug fixes & Enhancements

- Lyrics plugin now works when Swing Music is auto started (tested on Ubuntu)
- Track not being removed from queue
- Playlist list page moving out of bounds
- Save queue as playlist not working
- Keyboard shortcuts not working in first try
- Fix recently added items not filling row
- Fix recently added items order

# Development

- WIP code base documentation to `.github/docs`. Contributions are welcome!
- Bump watchdog to v4

> [!TIP]
> Plans for a mobile are underway. The development will be led by @EricGacoki