<template>
  <div class="l_ rounded" v-if="!props.collapsed">
    <div class="headin">Now Playing</div>
    <div class="menu image rounded"></div>
    <div class="separator no-border"></div>
    <div>
      <div class="art">
        <div
          class="l-image image rounded"
          :style="{
            backgroundImage: `url(&quot;${current.image}&quot;)`,
          }"
        ></div>
      </div>
      <div class="separator no-border"></div>
      <SongCard />
      <Progress />
      <HotKeys />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import state from "../../composables/state";
import SongCard from "./SongCard.vue";
import HotKeys from "../shared/HotKeys.vue";
import Progress from "../shared/Progress.vue";

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
  padding: 1rem;
  background-color: $primary;
  margin: $small;
  text-align: center;
  width: 14rem;
  display: grid;
  position: relative;
  text-transform: capitalize;

  .headin {
    font-weight: bold;
    font-size: 0.9rem;
  }

  .menu {
    height: 2rem;
    width: 2rem;
    right: $small;
    top: $small;
    position: absolute;
    background-image: url("../../assets/icons/right-arrow.svg");
    background-size: 1.5rem;
    transform: rotate(90deg);

    &:hover {
      background-color: $gray2;
    }
  }

  br {
    height: 0rem;
  }

  .art {
    width: 100%;
    display: grid;
    place-items: center;

    .l-image {
      height: 12rem;
      width: 12rem;
    }
  }

  .title {
    font-weight: 900;
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
