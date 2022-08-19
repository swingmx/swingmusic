import { ref } from "@vue/reactivity";
import { useIntersectionObserver } from "@vueuse/core";
import { Ref, watch } from "vue";

export default function useVisibility(
  elem: Ref<HTMLElement | null>,
  callback: (state: boolean) => void
) {
  const visible = ref(false);

  useIntersectionObserver(elem, ([{ isIntersecting }], observerElement) => {
    visible.value = isIntersecting;
  });

  watch(
    () => visible.value,
    (newVal) => {
      callback(newVal);
    }
  );
}
