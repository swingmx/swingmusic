# What's New?

<!-- TODO: ELABORATE -->
- Auth

## Improvements
- The context menu now doesn't take forever to open up
- Merged "Save as Playlist" with "Add to Playlist" > "New Playlist"

## Bug fixes
- Add to queue adding to last index -1
- 

## Development


## THE BIG ONE API CHANGES

- genre is no longer a string, but a struct:

```ts
interface Genre {
    name: str;
    genrehash: str;
}
```

