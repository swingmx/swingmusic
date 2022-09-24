function getElFullWidth(el: HTMLElement) {
  el.style.display = "inline-block";
  el.style.visibility = "hidden";
  document.getElementsByTagName("body")[0].appendChild(el);

  const width = el.offsetWidth;
  el.remove();

  return width;
}

export default (el: HTMLElement) => {
  const fullWidth = getElFullWidth(el.cloneNode(true) as HTMLElement);
  if (fullWidth <= el.offsetWidth) {
    el.title = "";
    return;
  }

  el.title = el.innerText;
};
