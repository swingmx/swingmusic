import { getElem } from "./perks";

export default (mouseX: number, mouseY: number) => {
  const scope = getElem("app", "id");
  const contextMenu = getElem("context-menu", "class");
  // ? compute what is the mouse position relative to the container element
  // (scope)
  let { left: scopeOffsetX, top: scopeOffsetY } = scope.getBoundingClientRect();

  scopeOffsetX = scopeOffsetX < 0 ? 0 : scopeOffsetX;
  scopeOffsetY = scopeOffsetY < 0 ? 0 : scopeOffsetY;

  const scopeX = mouseX - scopeOffsetX;
  const scopeY = mouseY - scopeOffsetY;

  // ? check if the element will go out of bounds
  const outOfBoundsOnX = scopeX + contextMenu.clientWidth > scope.clientWidth;

  const outOfBoundsOnY = scopeY + contextMenu.clientHeight > scope.clientHeight;

  let normalX = mouseX;
  let normalY = mouseY;
  let normalizedX = false;
  let normalizedY = false;

  if (window.innerWidth - normalX < 375) {
    normalizedX = true;
  }
  // ? normalize on X
  if (outOfBoundsOnX) {
    normalX = scopeOffsetX + scope.clientWidth - contextMenu.clientWidth;
    normalX -= 10;
  }

  // ? normalize on Y
  if (outOfBoundsOnY) {
    normalY = scopeOffsetY + scope.clientHeight - contextMenu.clientHeight;
    normalY -= 10;

    normalizedY = true;
  }

  return { normalX, normalY, normalizedX, normalizedY };
};
