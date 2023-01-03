// CREDITS: https://stackoverflow.com/a/66664192

/**
 * Scrolls and waits for the scroll to finish. Returns a promise that resolves when the scroll is finished.
 * @param elem The element to scroll and wait for
 * @param pos The position to scroll to
 * @param delay The delay in seconds to wait for
 * @returns A promise that resolves when the element has been scrolled to the position
 */
export default function waitForScrollEnd(
  elem: HTMLElement,
  pos = 0,
  delay = 100
): Promise<void> {
  elem.scroll({
    top: pos,
    behavior: "smooth",
  });
  const frame_limit = 20;
  let last_changed_frame = 0;
  let last_y = elem.scrollTop;

  return new Promise((resolve) => {
    function tick(frames: number) {
      // We requestAnimationFrame either for 500 frames or until 20 frames with
      // no change have been observed.
      if (frames >= 500 || frames - last_changed_frame > frame_limit) {
        setTimeout(() => {
          resolve();
        }, delay);
      } else {
        if (window.scrollY != last_y) {
          last_changed_frame = frames;
          last_y = window.scrollY;
        }
        requestAnimationFrame(tick.bind(null, frames + 1));
      }
    }
    tick(0);
  });
}
