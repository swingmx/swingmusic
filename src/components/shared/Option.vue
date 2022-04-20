<template>
  <div
    class="drop-btn rounded shadow-sm"
    id="option-drop"
    @click="showDropdown"
  >
    <div
      class="image drop-icon"
      :class="{ clicked: clicked && src == ContextSrc.PHeader }"
    ></div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { ContextSrc } from "../../composables/enums";

let elem: DOMRect;
const clicked = ref(false);

defineProps<{
  src?: string;
}>();

const emit = defineEmits<{
  (e: "showDropdown", event: any): void;
}>();

onMounted(() => {
  elem = document.getElementById("option-drop").getBoundingClientRect();
});

function showDropdown(e: Event) {
  e.preventDefault();
  e.stopImmediatePropagation();

  emit("showDropdown", {
    clientX: elem.left + 45,
    clientY: elem.top,
  });

  clicked.value = true;
}
</script>
<style lang="scss">
.drop-btn {
  width: 2.5rem;
  background-color: $accent;
  transition: all 0.5s ease-in-out;
  cursor: pointer;

  .drop-icon {
    transition: all 0.25s;
    padding: $small;
    height: 2.5rem;
    width: 2.5rem;
    background-image: url("../../assets/icons/right-arrow.svg");
    background-size: 1.75rem;
    transform: rotate(90deg);
  }

  .clicked {
    transform: rotate(0deg);
  }

  &:hover {
    background-color: $green;
    .image {
      transform: rotate(0deg);
    }
  }
}
</style>
