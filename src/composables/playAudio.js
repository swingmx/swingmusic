const playAudio = (path) => {
  const audio = new Audio("http://127.0.0.1:8901" + path);

  audio.addEventListener("canplaythrough", () => {
    audio.play();
  });
};

export { playAudio };
