import { ref } from "@vue/reactivity";

import perks from "./perks";

const audio = ref(new Audio()).value;
const pos = ref(0);

const url = "http://127.0.0.1:8901/";

const playAudio = (path) => {
  const full_path = url + encodeURIComponent(path);

  audio.src = full_path;

  audio.play();

  audio.ontimeupdate = () => {
    pos.value = audio.currentTime / audio.duration * 100;
  }

  audio.addEventListener("ended", () => {
    playNext();
  });
};

function playNext() {
  playAudio(perks.next.value.filepath);
  perks.current.value = perks.next.value;
}

function playPrev() {
  playAudio(perks.prev.value.filepath);
  perks.current.value = perks.prev.value;
}

function playPause() {
  if (audio.paused) {
    audio.play();
  } else {
    audio.pause();
  }
}

export default { playAudio, playNext, playPrev, playPause, pos };
