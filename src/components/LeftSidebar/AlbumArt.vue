<template>
  <div class="l_ rounded" v-if="!props.collapsed">
    <div
      class="l-image image rounded"
      :style="{
        backgroundImage: `url(&quot;${current.image}&quot;)`,
      }"
    ></div>
    <div class="separator no-border"></div>
    <SongCard />
  </div>
</template>

<script setup>
import { ref } from "vue";
import state from "../../composables/state";
import SongCard from "./SongCard.vue";

const current = ref(state.current);
const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});
</script>
<style lang="scss">
.l_ {
  padding: $small;
  background-color: #e24a01;
  margin: $small;

  .l-image {
    height: 13rem;
    width: 13rem;
  }

  .artists {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.808);

    &:hover {
      text-decoration: underline 1px !important;
    }
  }
}
</style>
