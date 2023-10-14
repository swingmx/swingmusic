![Image showing Post Malone](https://github.com/swing-opensource/swingmusic/assets/48554537/7ddcf688-7b49-4f8f-8a78-20685fb14f2f)

Swing Music v1.3.0 is **FINALLY** here!

## Release Summary

This release is ... _Bigger, Better, Faster, More!_

1. Related artists & albums
2. Mobile view (PWA)[`alpha`]
3. Album versions
4. Saving things as playlists
5. Adding things to playlists
6. Major UI redesign
7. Drop Ubuntu 18 support
8. Proper Docker support
9. Many bug fixes!

## Full Changelog

### What's New?
- Related artists - You can now explore related artists in the artist page
- Related albums - Explore albums similar to the current one, in the album page.
- Mobile port for the client - You can now use the web client in a mobile browser. For best experience, install it as a PWA on chromium browsers. If you’re not prompted to `Add Swing Music to Home screen` after ~30s on the app, click the 3 dots on the top right corner and select `Add to Home screen`.
  - You can also also install the client as a standalone app on desktop. Click the install button on the URL bar to install.
- Album versions - Explore other versions of an album at the bottom of the album tracklist.
- Recently added albums and artists in favorites page
- You can now use square images in playlist page. Open the update playlist dialog to toggle the feature per playlist.
- Save folder as playlist.
- Save album as playlist. Use album thumbnail as playlist image.
- Save artists as playlist. Use artist image as playlist image.
- Add folder/album/artist to playlist or queue
- Top results section in sidebar search and search page.
- Playlist page redesign to introduce large text.
- Join EP & Singles in artist page
- Make artist page with many albums faster
- TTY progress bars look a tiny bit consistent
- Make artist page faster (removed 100+ lines of 💩 code)
- Pinned playlists! You can now pin a playlist for quick access.
- New opt-in simple artist page header. Enable in settings.
- 8 new settings added to the settings page
  1. Artist separators
  2. Marking albums with one track as singles
  3. Simple artist page header
  4. Clean album titles
  5. Merge album versions
  6. Hide prod.
  7. Hide remaster info from tracks and albums
  10. Extract featured artists from metadata

### Enhancements

- Remove previous shuffle behavior (shuffling the queue only shuffled following tracks and moves the current one to the top of the queue)
- Better colors in page headers
- Always scan files on boot, even with the `-nps` (no periodic scans) flag.
- Redesign queue page to feature a large track thumbnail
- Show artist decade & genres in artist page
- Enhanced command line help text
- Swing Music process name now shows host and port
- Various UI redesigns and UX improvements.
  - Move to monochrome logos and color schemes
  - Search tab buttons and left sidebar items redesign
  - Better color schemes in album header and playlist page

### Bug Fixes

- Blank page on the browser on Windows caused by missing mime types.
- Ed Sheeran tracks being in a single album (due to their album names being only one non-alphanumeric character ... f**k Ed) you might lose some favorites though.
- Artist and album cards being cropped
- A lot more actually! I lost track of most of them.

##

Album of the Release • AUSTIN • [Listen on Spotify](https://open.spotify.com/album/6r1lh7fHMB499vGKtIyJLy)