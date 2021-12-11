const scrollLeftX = (artists_dom) => {
  const dom = artists_dom.value;
  dom.scrollBy({
    left: -700,
    behavior: "smooth",
  });
};

const scrollRightX = (artists_dom) => {
  const dom = artists_dom.value;
  dom.scrollBy({
    left: 700,
    behavior: "smooth",
  });
};

export { scrollLeftX, scrollRightX, };