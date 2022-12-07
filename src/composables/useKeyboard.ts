import useQStore from "@/stores/queue";

let key_down_fired = false;

function focusPageSearchBox() {
  const elem = document.getElementById(
    "page-search-trigger"
  ) as HTMLButtonElement;
  if (elem) {
    elem.dispatchEvent(new MouseEvent("click", { bubbles: false }));
  }
}

export default function (queue: typeof useQStore) {
  const q = queue();
  window.addEventListener("keydown", (e: KeyboardEvent) => {
    const target = e.target as HTMLElement;
    if (e.altKey) return;
    if (e.shiftKey) return;

    let ctrlKey = e.ctrlKey;

    function FocusedOnInput(target: HTMLElement) {
      return target.tagName === "INPUT" || target.tagName === "TEXTAREA";
    }

    if (FocusedOnInput(target)) return;

    switch (e.key) {
      case "ArrowRight":
        {
          if (!key_down_fired) {
            key_down_fired = true;

            setTimeout(() => {
              key_down_fired = false;
            }, 1000);

            q.playNext();
          }
        }
        break;

      case "ArrowLeft":
        {
          if (!key_down_fired) {
            key_down_fired = true;

            q.playPrev();

            setTimeout(() => {
              key_down_fired = false;
            }, 1000);
          }
        }

        break;

      case " ":
        {
          if (!key_down_fired) {
            e.preventDefault();
            key_down_fired = true;

            q.playPause();
          }
        }

        break;

      case "f": {
        if (!key_down_fired) {
          if (!ctrlKey) return;
          e.preventDefault();
          focusPageSearchBox();

          key_down_fired = true;
        }
      }
    }
  });
}

window.addEventListener("keyup", () => {
  key_down_fired = false;
});
