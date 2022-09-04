import { Directive } from "vue";
import { createPopper } from "@popperjs/core";

let tooltip: HTMLElement;

export default {
  mounted(el, binding) {
    let isHovered = false;
    const tooltip = document.getElementById("tooltip") as HTMLElement;

    el.addEventListener("mouseover", () => {
      isHovered = true;

      setTimeout(() => {
        if (isHovered) {
          tooltip.innerText = binding.value;
          tooltip.style.display = "unset";

          createPopper(el, tooltip, {
            placement: "top",
            modifiers: [
              {
                name: "offset",
                options: {
                  offset: [0, 10],
                },
              },
            ],
          });
        }
      }, 1500);
    });

    el.addEventListener("mouseout", () => {
      isHovered = false;
      tooltip.style.display = "none";
    });
  },
  beforeUnmount(el: HTMLElement) {
    const tooltip = document.getElementById("tooltip") as HTMLElement;
    tooltip.style.display = "none";

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
  },
} as Directive;
