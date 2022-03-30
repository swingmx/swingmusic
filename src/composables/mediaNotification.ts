import { Track } from "../interfaces.js";
import perks from "./perks.js";

export default (
  track: Track,
  playPause: () => void,
  playNext: () => void,
  playPrev: () => void
) => {
  if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new window.MediaMetadata({
      title: track.title,
      artist: track.artists.join(", "),
      artwork: [
        {
          src: track.image,
          sizes: "96x96",
          type: "image/jpeg",
        },
        {
          src: track.image,
          sizes: "128x128",
          type: "image/webp",
        },
        {
          src: track.image,
          sizes: "192x192",
          type: "image/webp",
        },
        {
          src: track.image,
          sizes: "256x256",
          type: "image/webp",
        },
        {
          src: track.image,
          sizes: "384x384",
          type: "image/webp",
        },
        {
          src: track.image,
          sizes: "512x512",
          type: "image/webp",
        },
      ],
    });

    navigator.mediaSession.setActionHandler("play", function () {
      playPause();
    });
    navigator.mediaSession.setActionHandler("pause", function () {
      playPause();
    });
    navigator.mediaSession.setActionHandler("previoustrack", function () {
      playPrev();
    });
    navigator.mediaSession.setActionHandler("nexttrack", function () {
      playNext();
    });
  }
};
