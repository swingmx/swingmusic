import { computed } from "vue";
import { ref } from "@vue/reactivity";

const content_width = ref(0);
const window_width = ref(0);

const isSmall = computed(() => {
  return content_width.value < 700;
});

export { content_width, window_width, isSmall };
