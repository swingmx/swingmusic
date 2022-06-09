import { playSources } from "@/composables/enums";

import useQStore from "@/stores/queue";
import useFStore from "@/stores/folder";
import useAStore from "@/stores/album";
import usePStore from "@/stores/p.ptracks";

const queue = useQStore;
const folder = useFStore;
const album = useAStore;
const playlist = usePStore;

type store = typeof queue | typeof folder | typeof album | typeof playlist;

export default function play(
  source: playSources,
  aqueue: typeof queue,
  store: store
) {
  const useQueue = aqueue();

  switch (source) {
    // check which route the play request come from
    case playSources.folder:
      store = store as typeof folder;

      useQueue.playFromFolder(store().path, store().tracks);
      useQueue.play(store().tracks[0]);
      break;
    case playSources.album:
      store = store as typeof album;

      useQueue.playFromAlbum(
        store().info.title,
        store().info.artist,
        store().tracks
      );
      useQueue.play(store().tracks[0]);
      break;
    case playSources.playlist:
      store = store as typeof playlist;

      useQueue.playFromPlaylist(
        store().info.name,
        store().info.playlistid,
        store().tracks
      );
      useQueue.play(store().tracks[0]);
      break;
  }
}
