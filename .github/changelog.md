Swing Music v1.3.0 is **FINALLY** here!

## Summary

This release is ... _Bigger, Better, Faster, More!_

1. Related artists & albums
2. Mobile view (PWA)[`alpha`]
3. Album versions
4. Saving things as playlists
5. Adding things to playlists
6. Major UI redesign
7. Many bug fixes!

## Full Changelog

### What's New?

- Related artists - You can now explore related artists in the artist page
- Related albums - Explore albums similar to the current one, in the album page.
- Mobile port for the client - You can now use the web client in a mobile browser. For best experience, install it as a PWA on chromium browsers. If you’re not prompted to `Add Swing Music to Home screen` after ~30s on the app, click the 3 dots on the top right corner and select `Add to Home screen`.
  - You can also also install the client as a standalone app on desktop. Click the install button on the URL to install.
- Album versions - Explore other versions of an album at the bottom of the album tracklist.
- Recently added in favorites page
- You can now use square images in playlist page. Open the update playlist dialog to toggle the feature per playlist.
- Save folder as playlist.
- Save album as playlist. Use album thumbnail as playlist image.
- Save artists as playlist. Use artist image as playlist image.
- Add folder/album/artist to playlist or queue
- Top results section in sidebar search and search page.
- Playlist page redesign to introduce header.
- Pinned playlists! You can now pin a playlist for quick access.
- New opt-in simple artist page header. Enable in settings.
- 8 new settings added to the settings page
  1. Artist separators
  2. Marking albums with one track as singles
  3. Simple artist page header
  4. Clean album titles
  5. Merge album versions
  6. Hide prod.
  7. Hide remaster info
  8. Extract featured artists

### Enhancements

- Remove previous shuffle behavior shuffling the queue only shuffled following tracks and moves the current one to the top of the queue.
- Better colors in page headers
- Run the populate function on boot, even with the `-nps` (no periodic scans) flag.
- Redesign queue page
- Show artist decade & genres in artist page
- Better command line help text
- Code enhancements
- Swing Music process naming
- Various UI redesigns and UX improvements.
  - Less pink, more white.
  - Search tab buttons and left sidebar items redesign
  - Better color schemes in album header and playlist page

### Bug Fixes

- Blank page on the browser on Windows caused by missing mime types.
- Artist and album cards being cropped
- A lot more actually! I lost track of most of them.
