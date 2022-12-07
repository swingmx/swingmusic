import { playSources } from "@/composables/enums";

import useAStore from "@/stores/pages/album";
import useArtistPageStore from "@/stores/pages/artist";
import useFStore from "@/stores/pages/folder";
import usePStore from "@/stores/pages/playlist";
import useQStore from "@/stores/queue";
import useSettingsStore from "@/stores/settings";
import { useNotifStore } from "@/stores/notification";

import { getArtistTracks } from "./fetch/artists";
import { getAlbumTracks } from "./fetch/album";

const queue = useQStore;
const folder = useFStore;
const album = useAStore;
const playlist = usePStore;
const artist = useArtistPageStore;

type store =
  | typeof queue
  | typeof folder
  | typeof album
  | typeof playlist
  | typeof artist;

export default async function play(
  source: playSources,
  aqueue: typeof queue,
  store: store
) {
  const useQueue = aqueue();

  switch (source) {
    // check which route the play request come from
    // case playSources.folder:
    //   store = store as typeof folder;
    //   const f = store();

    //   useQueue.playFromFolder(f.path, f.tracks);
    //   useQueue.play();
    //   break;
    case playSources.album:
      store = store as typeof album;
      const a_store = store();

      useQueue.playFromAlbum(
        a_store.info.title,
        a_store.info.albumhash,
        a_store.allTracks
      );
      useQueue.play();
      break;
    case playSources.playlist:
      store = store as typeof playlist;
      const p = store();

      if (p.tracks.length === 0) return;

      useQueue.playFromPlaylist(p.info.name, p.info.id, p.tracks);
      useQueue.play();
      break;

    case playSources.artist:
      store = store as typeof artist;
      utilPlayFromArtist(useQStore, useArtistPageStore, 0);
  }
}

async function utilPlayFromArtist(
  queue: typeof useQStore,
  artist: typeof useArtistPageStore,
  index: number = 0
) {
  const qu = queue();
  const ar = artist();
  const settings = useSettingsStore();

  if (ar.tracks.length === 0) return;

  if (ar.info.trackcount <= settings.artist_top_tracks_count) {
    qu.playFromArtist(ar.info.artisthash, ar.info.name, ar.tracks);
    qu.play();
    return;
  }

  const tracks = await getArtistTracks(ar.info.artisthash);

  qu.playFromArtist(ar.info.artisthash, ar.info.name, tracks);
  qu.play(index);
}

async function playFromAlbumCard(
  queue: typeof useQStore,
  albumhash: string,
  albumname: string
) {
  const qu = queue();

  const tracks = await getAlbumTracks(albumhash, useNotifStore);
  qu.playFromAlbum(albumname, albumhash, tracks.tracks);
  qu.play();
}

export { utilPlayFromArtist, playFromAlbumCard };
