import { paths } from "../config";

import useQueueStore from "../stores/queue";

export default () => {
  if ("mediaSession" in navigator) {
    const queue = useQueueStore();
    const { currenttrack: track } = queue;

    if (track === undefined) {
      return;
    }

    const url = paths.images.thumb.large;

    navigator.mediaSession.metadata = new window.MediaMetadata({
      title: track.title,
      artist: track.artist.map((a) => a.name).join(", "),
      artwork: [
        {
          src: url + track.image,
          sizes: "96x96",
          type: "image/jpeg",
        },
        {
          src: url + track.image,
          sizes: "128x128",
          type: "image/webp",
        },
        {
          src: url + track.image,
          sizes: "192x192",
          type: "image/webp",
        },
        {
          src: url + track.image,
          sizes: "256x256",
          type: "image/webp",
        },
        {
          src: url + track.image,
          sizes: "384x384",
          type: "image/webp",
        },
        {
          src: url + track.image,
          sizes: "512x512",
          type: "image/webp",
        },
      ],
    });

    navigator.mediaSession.setActionHandler("play", () => {
      queue.playPause();
    });
    navigator.mediaSession.setActionHandler("pause", () => {
      queue.playPause();
    });
    navigator.mediaSession.setActionHandler("previoustrack", () => {
      queue.playPrev();
    });
    navigator.mediaSession.setActionHandler("nexttrack", () => {
      queue.playNext();
    });
  }
};
