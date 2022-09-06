import { Directive, Ref, ref } from "vue";
import { createPopper } from "@popperjs/core";

let tooltip: HTMLElement;

function getTooltip() {
  return document.getElementById("tooltip") as HTMLElement;
}

function hideTooltip() {
  tooltip.style.visibility = "hidden";
}

function handleHover(el: HTMLElement, text: string, isHovered: Ref<boolean>) {
  el.addEventListener("mouseover", () => {
    isHovered.value = true;
    tooltip.innerText = text;

    setTimeout(() => {
      if (isHovered.value) {
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
    }, 2000);
  });
}
let isHovered = ref(false);

export default {
  state: {},
  mounted(el: HTMLElement, binding) {
    if (tooltip === undefined) {
      tooltip = getTooltip();
    }

    handleHover(el, binding.value, isHovered);
    ["mouseout", "click"].forEach((event) => {
      el.addEventListener(event, () => {
        isHovered.value = false;
        hideTooltip();
      });
    });
  },
  updated(el, binding) {
    el.removeEventListener("mouseover", () => {});
    handleHover(el, binding.value, isHovered);
  },
  beforeUnmount(el: HTMLElement) {
    hideTooltip();

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
  },
} as Directive;
