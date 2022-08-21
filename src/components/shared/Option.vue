<template>
  <button id="option-drop" @click.stop.prevent="showDropdown" class="btn-more">
    <MoreSvg />
  </button>
</template>
<script setup lang="ts">
import { onMounted } from "vue";
import MoreSvg from "../../assets/icons/more.svg";
let elem: DOMRect;

const props = defineProps<{
  src?: string;
}>();

const emit = defineEmits<{
  (e: "showDropdown", event: any): void;
}>();

onMounted(() => {
  const el = document.getElementById("option-drop") as HTMLElement;
  elem = el.getBoundingClientRect();
});

function showDropdown(e: Event) {
  if (!props.src) return;

  emit("showDropdown", {
    clientX: elem.left + 35,
    clientY: elem.top,
  });
}
</script>
