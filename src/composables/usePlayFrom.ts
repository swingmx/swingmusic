import { playSources } from "@/composables/enums";
import useAStore from "@/stores/pages/album";
import useFStore from "@/stores/pages/folder";
import usePStore from "@/stores/pages/playlist";
import useQStore from "@/stores/queue";

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
      const f = store();

      useQueue.playFromFolder(f.path, f.tracks);
      useQueue.play(f.tracks[0]);
      break;
    case playSources.album:
      store = store as typeof album;
      const a = store();

      useQueue.playFromAlbum(a.info.title, a.info.artist, a.tracks);
      useQueue.play(store().tracks[0]);
      break;
    case playSources.playlist:
      store = store as typeof playlist;
      const p = store();

      if (p.tracks.length === 0) return;

      useQueue.playFromPlaylist(p.info.name, p.info.playlistid, p.tracks);
      useQueue.play(store().tracks[0]);
      break;
  }
}
