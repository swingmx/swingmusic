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
      tooltip.style.visibility = "hidden";
    });
  },
  beforeUnmount(el: HTMLElement) {
    const tooltip = document.getElementById("tooltip") as HTMLElement;
    tooltip.style.visibility = "hidden";

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
    
  },
} as Directive;
