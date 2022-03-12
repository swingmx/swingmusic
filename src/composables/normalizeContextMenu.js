import perks from "./perks";

export default function normalizeContextMenu(x, y) {
  const app_dom = perks.getElem("app", "id");
  const context_menu = perks.getElem("context-menu-visible", "class");

  const { left: scopeOffsetX, top: scopeOffsetY } =
    app_dom.getBoundingClientRect();

  const scopeX = x - scopeOffsetX;
  const scopeY = y - scopeOffsetY;

  const outOfBoundsX = scopeX + context_menu.clientHeight > app_dom.clientWidth;
  const outOfBoundsY =
    scopeY + context_menu.clientHeight > app_dom.clientHeight;

  let normalizedX = x;
  let normalizedY = y;

  if (outOfBoundsX) {
    normalizedX =
      scopeOffsetX + app_dom.clientWidth - context_menu.clientHeight;
  }

  if (outOfBoundsY) {
    normalizedY =
      scopeOffsetY + app_dom.clientHeight - context_menu.clientHeight;
  }

  return {
    normalizedX,
    normalizedY,
  };
}
