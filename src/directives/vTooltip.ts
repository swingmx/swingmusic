import { Directive } from "vue";
import { createPopper, Instance, VirtualElement } from "@popperjs/core";

let tooltip: HTMLElement;
let popperInstance: Instance;
let store: any;

// @ts-ignore
const virtualEl = {
  getBoundingClientRect: () => new DOMRect(),
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

function getFullWidth(el: HTMLElement) {
  // display el as inline-block to get the correct width
  el.style.display = "inline-block";
  el.style.visibility = "hidden";
  document.getElementsByTagName("body")[0].appendChild(el);
  const width = el.offsetWidth;
  el.remove();

  return width;
}

export default (el: HTMLElement) => {
  const fullWidth = getFullWidth(el.cloneNode(true) as HTMLElement);
  if (fullWidth <= el.offsetWidth) return;

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
};

// } as Directive;

// beforeUnmount(el: HTMLElement) {
//   // hideTooltip();

//   el.removeEventListener("mouseover", () => {});
//   el.removeEventListener("mouseout", () => {});
// },
