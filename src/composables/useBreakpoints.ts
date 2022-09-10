import { useBreakpoints, breakpointsTailwind } from "@vueuse/core";

const breakpoints = useBreakpoints(breakpointsTailwind);

const xl = breakpoints.greater("xl");

export { xl };
