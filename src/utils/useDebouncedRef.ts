import { customRef, Ref, ref } from "vue";

/**
 * Debounces a function
 *
 * @param {*} fn The function to debounce
 * @param {*} delay The delay in milliseconds
 * @param {*} immediate whether to debounce immediately
 */
const debounce = (
  fn: (...params: any) => void,
  delay: number = 0,
  immediate: any = false
) => {
  let timeout: any;
  return (...args: any) => {
    if (immediate && !timeout) fn(...args);
    clearTimeout(timeout);

    timeout = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

/**
 * Emits the ref updated value after the given delay.
 *
 * @param {*} initialValue The default value of the ref
 * @param {*} delay The delay in milliseconds
 * @param {*} immediate Whether to call the function immediately
 * @returns {Object} The ref and a function to call to update the ref
 */
const useDebouncedRef = (
  initialValue: string,
  delay: number,
  immediate = false
) => {
  const state = ref(initialValue);
  return customRef((track, trigger) => ({
    get() {
      track();
      return state.value;
    },
    set: debounce(
      (value) => {
        state.value = value;
        trigger();
      },
      delay,
      immediate
    ),
  }));
};

export default useDebouncedRef;
