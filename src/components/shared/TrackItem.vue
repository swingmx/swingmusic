<template>
  <div
    class="track-item h-1"
    @click="playThis(props.track)"
    :class="[
      {
        currentInQueue: props.isCurrent,
      },
      { 'context-on': context_on },
    ]"
    @contextmenu="showContextMenu"
  >
    <div
      class="album-art image rounded"
      :style="{
        backgroundImage: `url(&quot;${imguri + props.track.image}&quot;)`,
      }"
    >
      <div
        class="now-playing-track image"
        v-if="props.isCurrent"
        :class="{ active: props.isPlaying, not_active: !props.isPlaying }"
      ></div>
    </div>
    <div class="tags">
      <div class="title ellip">{{ props.track.title }}</div>
      <hr />
      <div class="artist ellip">
        <span v-for="artist in putCommas(props.track.artists)" :key="artist">{{
          artist
        }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import perks from "../../composables/perks";
import trackContext from "../../contexts/track_context";
import { Track } from "../../interfaces";
import { ContextSrc } from "../../composables/enums";

import useContextStore from "../../stores/context";
import useModalStore from "../../stores/modal";
import useQueueStore from "../../stores/queue";
import { paths } from "../../config";


const contextStore = useContextStore();
const imguri = paths.images.thumb

const props = defineProps<{
  track: Track;
  isCurrent: boolean;
  isPlaying: boolean;
}>();

const context_on = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(props.track, useModalStore, useQueueStore);

  contextStore.showContextMenu(e, menus, ContextSrc.Track);
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
    }
  });
};

const emit = defineEmits<{
  (e: "PlayThis", track: Track): void;
}>();

const current = ref(perks.current);
const putCommas = perks.putCommas;

const playThis = (track: Track) => {
  emit("PlayThis", track);
};
</script>

<style lang="scss">
.currentInQueue {
  background-color: $gray3;
}

.context-on {
  background-color: $gray4;
  color: $white !important;
}

.track-item {
  display: flex;
  align-items: center;
  border-radius: 0.5rem;
  position: relative;
  height: 4rem;
  padding: 0.5rem 0.5rem 0.5rem 4rem;

  &:hover {
    cursor: pointer;
    background-color: $gray4 !important;
  }

  hr {
    border: none;
    margin: 0.1rem;
  }

  .album-art {
    position: absolute;
    left: $small;
    display: flex;
    align-items: center;
    justify-content: center;

    width: 3rem;
    height: 3rem;
    margin: 0 0.5rem 0 0;
    background-image: url(../../assets/images/null.webp);
  }
  .artist {
    font-size: small;
    color: rgba(255, 255, 255, 0.637);
  }
}
</style>
