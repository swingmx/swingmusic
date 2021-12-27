import perks from "./perks.js";
import playAudio from "./playAudio.js";

let showMediaNotif = () => {
  let current = perks.current.value;

  if ("mediaSession" in navigator) {
    navigator.mediaSession.metadata = new window.MediaMetadata({
      title: current.title,
      artist: current.artists,
      artwork: [
        {
          src: current.image,
          sizes: "96x96",
          type: "image/jpeg",
        },
        {
          src: current.image,
          sizes: "128x128",
          type: "image/png",
        },
        {
          src: current.image,
          sizes: "192x192",
          type: "image/png",
        },
        {
          src: current.image,
          sizes: "256x256",
          type: "image/png",
        },
        {
          src: current.image,
          sizes: "384x384",
          type: "image/png",
        },
        {
          src: current.image,
          sizes: "512x512",
          type: "image/png",
        },
      ],
    });

    navigator.mediaSession.setActionHandler("play", function () {
      playAudio.playPause();
    });
    navigator.mediaSession.setActionHandler("pause", function () {
      playAudio.playPause();
    });
    navigator.mediaSession.setActionHandler("seekbackward", function () {});
    navigator.mediaSession.setActionHandler("seekforward", function () {});
    navigator.mediaSession.setActionHandler("previoustrack", function () {
      playAudio.playPrev();
    });
    navigator.mediaSession.setActionHandler("nexttrack", function () {
      playAudio.playNext();
    });
  }
};

export default {
  showMediaNotif,
};
