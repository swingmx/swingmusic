const itemWidth = 160;
const itemMarginBottom = 24;

export default (containerWidth = 0, containerHeight = 0) => {
  return Math.floor(containerWidth / itemWidth);
};
