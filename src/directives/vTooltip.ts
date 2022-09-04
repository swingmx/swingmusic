import { Directive } from "vue";
import { createPopper } from "@popperjs/core";

export default {
  mounted(el, binding) {
    let isHovered = false;
    const tooltip = document.getElementById("tooltip") as HTMLElement;

    el.addEventListener("mouseenter", () => {
      isHovered = true;

      setTimeout(() => {
        tooltip.innerText = binding.value;

        if (isHovered) {
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
      }, 1000);
    });

    el.addEventListener("mouseleave", () => {
      isHovered = false;
      tooltip.style.display = "none";
    });
  },
  beforeUnmount(el: HTMLElement) {
    el.removeEventListener("mouseenter", () => {});
    el.removeEventListener("mouseleave", () => {});
  },
} as Directive;
