import { Directive } from "vue";
import { createPopper } from "@popperjs/core";

let tooltip: HTMLElement;

function getTooltip() {
  return document.getElementById("tooltip") as HTMLElement;
}

function hideTooltip() {
  tooltip.style.visibility = "hidden";
}

export default {
  updated(el, binding) {
    let isHovered = false;

    if (tooltip === undefined) {
      tooltip = getTooltip();
    }

    el.addEventListener("mouseover", () => {
      isHovered = true;

      setTimeout(() => {
        if (isHovered) {
          tooltip.innerText = binding.value;
          tooltip.style.visibility = "visible";

          createPopper(el, tooltip, {
            placement: "top",
            modifiers: [
              {
                name: "offset",
                options: {
                  offset: [0, 10],
                },
              },
              {
                name: "hide",
                enabled: true,
              },
            ],
          });
        }
      }, 1500);
    });

    el.addEventListener("mouseout", () => {
      isHovered = false;
      hideTooltip();
    });
  },
  beforeUnmount(el: HTMLElement) {
    hideTooltip();

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
  },
} as Directive;
