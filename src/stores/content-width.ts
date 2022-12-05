import { computed } from "vue";
import { ref } from "@vue/reactivity";

const content_width = ref(0);
const window_width = ref(0);

const brk = {
  small: 600,
  medium: 950,
  album_header_small: 700,
};

const isSmall = computed(() => {
  return content_width.value <= brk.small;
});

const isMedium = computed(() => {
  return content_width.value > brk.small && content_width.value <= brk.medium;
});

const albumHeaderSmall = computed(() => {
  return content_width.value <= brk.album_header_small;
});
const album_card_with = 10 * 16;

const maxAbumCards = computed(() => {
  return Math.floor(content_width.value / album_card_with);
});

export {
  content_width,
  window_width,
  isSmall,
  isMedium,
  albumHeaderSmall,
  maxAbumCards,
};
