import { ref } from "@vue/reactivity";

const audio = ref(new Audio()).value;

const playAudio = (path) => {
  const full_path = "http://127.0.0.1:8901/" + encodeURIComponent(path);

  audio.src = full_path;
  audio.addEventListener("canplaythrough", () => {
    audio.play();
  });
};

export { playAudio };
