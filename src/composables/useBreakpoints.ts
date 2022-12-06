import { useBreakpoints } from "@vueuse/core";

const breakpoints = useBreakpoints({
  xl: 1280,
  xxl: 1720,
});

const xl = breakpoints.greater("xl");
const xxl = breakpoints.greater("xxl");

export { xl, xxl };
