export function handlePlayPause(
  currentIndex: number,
  audio: HTMLAudioElement,
  state: boolean,
  play: (index: number) => void
) {
  if (audio.src === "") {
    play(currentIndex);
  } else if (audio.paused) {
    audio.play();
    state = true;
  } else {
    audio.pause();
    state = false;
  }
}
