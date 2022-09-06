import { Directive, Ref, ref } from "vue";
import { createPopper } from "@popperjs/core";

let tooltip: HTMLElement;

function getTooltip() {
  return document.getElementById("tooltip") as HTMLElement;
}

function hideTooltip() {
  tooltip.style.visibility = "hidden";
}

function handleHover(el: HTMLElement, text: string, handleOthers = true) {
  let isHovered = false;

  el.addEventListener("mouseover", () => {
    isHovered = true;
    tooltip.innerText = text;

    setTimeout(() => {
      if (isHovered) {
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

    function handleHide() {
      ["mouseout", "click"].forEach((event) => {
        el.addEventListener(event, () => {
          isHovered = false;
          hideTooltip();
        });
      });
    }

    handleOthers ? handleHide() : null;
  });
}
let isHovered = ref(false);

export default {
  mounted(el: HTMLElement, binding) {
    if (tooltip === undefined) {
      tooltip = getTooltip();
    }

    handleHover(el, binding.value);
  },
  updated(el, binding) {
    el.removeEventListener("mouseover", () => {});
    handleHover(el, binding.value, false);
  },
  beforeUnmount(el: HTMLElement) {
    hideTooltip();

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
  },
} as Directive;
