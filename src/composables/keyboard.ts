import { Store } from "pinia";

let key_down_fired = false;

function focusSearchBox() {
  const elem = document.getElementById("search");

  elem.focus();
}

export default function (queue: any) {
  window.addEventListener("keydown", (e: any) => {
    let target = e.target;
    let ctrlKey = e.ctrlKey;

    switch (e.key) {
      case "ArrowRight":
        if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;

        {
          if (!key_down_fired) {
            key_down_fired = true;

            setTimeout(() => {
              key_down_fired = false;
            }, 1000);

            queue.playNext();
          }
        }
        break;

      case "ArrowLeft":
        {
          if (!key_down_fired) {
            if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;

            key_down_fired = true;

            queue.playPrev();

            setTimeout(() => {
              key_down_fired = false;
            }, 1000);
          }
        }

        break;

      case " ":
        {
          if (!key_down_fired) {
            if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;
            e.preventDefault();
            key_down_fired = true;

            queue.playPause();
          }
        }

        break;

      case "f": {
        if (!key_down_fired) {
          if (!ctrlKey) return;
          e.preventDefault();


          key_down_fired = true;
        }
      }
      case "/": {{
        e.preventDefault();
        focusSearchBox();
      }}
    }
  });
}

window.addEventListener("keyup", () => {
  key_down_fired = false;
});
