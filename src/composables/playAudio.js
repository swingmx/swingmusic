import { ref } from "@vue/reactivity";

import perks from "./perks";

const audio = ref(new Audio()).value;
const pos = ref(0);
const playing = ref(false)

const url = "http://127.0.0.1:8901/";

const playAudio = (path) => {
  const full_path = url + encodeURIComponent(path);

  setTimeout(() => {
    audio.src = full_path;
  }, 150);
  audio.load();

  audio.oncanplaythrough = () => {
    audio.play();
  };

  audio.ontimeupdate = () => {
    pos.value = (audio.currentTime / audio.duration) * 1000;
  };

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

function seek(pos) {
  console.log(pos);
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

audio.addEventListener('play', () => {
  playing.value = true;
})

audio.addEventListener('pause', () => {
  playing.value = false;
})

export default { playAudio, playNext, playPrev, playPause, seek, pos, playing };
