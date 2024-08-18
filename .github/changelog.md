# What's New?

<!-- TODO: ELABORATE -->

- Auth
- New artists/albums Sort by: last played, no. of streams, total stream duration
- Option to show now playing track info on tab title. Go to Settings > Appearance to enable
- You can select which disc to play in an album
- Internal Backup and restore

## Improvements

- The context menu now doesn't take forever to open up
- Merged "Save as Playlist" with "Add to Playlist" > "New Playlist"

## Bug fixes

- Add to queue adding to last index -1

## Development

- Rewritten the whole DB layer to move stores from memory to the database.

## THE BIG ONE API CHANGES

- genre is no longer a string, but a struct:

```ts
interface Genre {
  name: str;
  genrehash: str;
}
```

- Pairing via QR Code has been split into 2 endpoint:

  1. `/getpaircode`
  2. `/pair`

-
