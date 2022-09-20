import { Directive } from "vue";
import { createPopper, Instance, VirtualElement } from "@popperjs/core";

let tooltip: HTMLElement;
let popperInstance: Instance;
let store: any;

// @ts-ignore
const virtualEl = {
  getBoundingClientRect: () => null,
} as VirtualElement;

const getTooltip = () => document.getElementById("tooltip") as HTMLElement;

function getInstance() {
  if (tooltip && virtualEl) {
    return createPopper(virtualEl, getTooltip(), {
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
        {
          name: "eventListeners",
          enabled: false,
        },
      ],
    });
  }

  return null;
}

function showTooltip() {
  tooltip.style.visibility = "visible";
}

function hideTooltip() {
  tooltip.style.visibility = "hidden";
}

export default {
  mounted(el: HTMLElement, binding) {
    if (!tooltip) {
      tooltip = getTooltip();
    }

    if (!popperInstance) {
      popperInstance = getInstance() as Instance;
    }

    let isHovered = false;

    el.addEventListener("mouseover", () => {
      isHovered = true;

      setTimeout(() => {
        if (!isHovered) return;
        tooltip.innerText = el.innerText;

        virtualEl.getBoundingClientRect = () => el.getBoundingClientRect();
        popperInstance.update().then(showTooltip);
      }, 1500);
    });

    ["mouseout", "click"].forEach((event) => {
      document.addEventListener(event, () => {
        isHovered = false;
        hideTooltip();
      });
    });
  },
  beforeUnmount(el: HTMLElement) {
    hideTooltip();

    el.removeEventListener("mouseover", () => {});
    el.removeEventListener("mouseout", () => {});
  },
} as Directive;
