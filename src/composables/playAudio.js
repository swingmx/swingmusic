import { ref } from "@vue/reactivity";

import perks from "./perks";
import media from "./mediaNotification.js";
import state from "./state.js";

const audio = ref(new Audio()).value;
const pos = ref(0);
const playing = ref(state.is_playing);

const url = "http://0.0.0.0:8901/";

const playAudio = (path) => {
  const full_path = url + encodeURIComponent(path);

  new Promise((resolve, reject) => {
    audio.src = full_path;
    audio.oncanplaythrough = resolve;
    audio.onerror = reject;
  })
    .then(() => {
      audio.play();
      perks.focusCurrent()

      state.is_playing.value = true;

      audio.ontimeupdate = () => {
        pos.value = (audio.currentTime / audio.duration) * 1000;
        
      };
    })
    .catch((err) => console.log(err));
};

function playNext() {
  playAudio(perks.next.value.filepath);
  perks.current.value = perks.next.value;
  media.showMediaNotif();
}

function playPrev() {
  playAudio(perks.prev.value.filepath);
  perks.current.value = perks.prev.value;
}

function seek(pos) {
  audio.currentTime = (pos / 1000) * audio.duration;
}

function playPause() {
  if (audio.src === "") {
    playAudio(perks.current.value.filepath);
  }

  if (audio.paused) {
    audio.play();
  } else {
    audio.pause();
  }
}

audio.addEventListener("play", () => {
  state.is_playing.value = true;
});

audio.addEventListener("pause", () => {
  state.is_playing.value = false;
});

audio.addEventListener("ended", () => {
  playNext();
});

export default { playAudio, playNext, playPrev, playPause, seek, pos, playing };


// TODO
// Try implementing classes to play audio .ie. Make the seek, playNext, playPrev, etc the methods of a class. etc
