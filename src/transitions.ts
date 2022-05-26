export default {
  directives: {
    "slide-from-left": {
      initial: {
        opacity: 0,
        x: 0,
        y: 20
      },
      enter: {
        opacity: 1,
        x: 0,
        y: 0,
        transition: {
          duration: 100,
          ease: "circInOut",
        },
      },
    },
    "slide-from-left-100": {
      initial: {
        opacity: 0,
        x: -20,
      },
      enter: {
        opacity: 1,
        x: 0,
        transition: {
          delay: 100,
        },
      },
    },
    "slide-from-top": {
      initial: {
        y: -20,
        opacity: 0,
      },
      enter: {
        y: 0,
        opacity: 1,
        transition: {
          delay: 200,
        },
      },
    },
    "slide-from-right": {
      initial: {
        x: 20,
        opacity: 0,
      },
      enter: {
        x: 0,
        opacity: 1,
        transition: {
          delay: 200,
        },
      },
    },
    scale: {
      initial: {
        scale: 0.8,
      },
      enter: {
        scale: 1,
        transition: {
          duration: 200,
        },
      },
    },
  },
};
