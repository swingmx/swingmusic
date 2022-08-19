import { Track } from "../interfaces.js";
import { paths } from "../config";

import useQueueStore from "../stores/queue";

export default () => {
  if ("mediaSession" in navigator) {
    const queue = useQueueStore();

    navigator.mediaSession.metadata = new window.MediaMetadata({
      title: queue.currenttrack.title,
      artist: queue.currenttrack.artists.join(", "),
      artwork: [
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "96x96",
          type: "image/jpeg",
        },
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "128x128",
          type: "image/webp",
        },
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "192x192",
          type: "image/webp",
        },
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "256x256",
          type: "image/webp",
        },
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "384x384",
          type: "image/webp",
        },
        {
          src: paths.images.thumb + queue.currenttrack.image,
          sizes: "512x512",
          type: "image/webp",
        },
      ],
    });

    navigator.mediaSession.setActionHandler("play", function () {
      queue.playPause();
    });
    navigator.mediaSession.setActionHandler("pause", function () {
      queue.playPause();
    });
    navigator.mediaSession.setActionHandler("previoustrack", function () {
      queue.playPrev();
    });
    navigator.mediaSession.setActionHandler("nexttrack", function () {
      queue.playNext();
    });
  }
};
