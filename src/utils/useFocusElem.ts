/**
 * Scrolls a element into view.
 * @param className The class to focus
 * @param delay Delay in milliseconds
 * @param pos Positioning of the focus element
 */
export default function focusElemByClass(
  className: string,
  delay?: number,
  pos?: any
) {
  const dom = document.getElementsByClassName(className)[0];

  setTimeout(() => {
    if (dom) {
      dom.scrollIntoView({
        behavior: "smooth",
        block: `${pos ?? "start"}` as any,
        inline: "center",
      });
    }
  }, delay || 300);
}
