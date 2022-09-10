import { computed } from "vue";
import { ref } from "@vue/reactivity";

const content_width = ref(0);

const isSmall = computed(() => {
  return content_width.value < 700;
});

console.log(content_width);
export { content_width, isSmall };
