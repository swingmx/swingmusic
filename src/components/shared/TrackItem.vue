<template>
  <div
    class="track-item"
    @click="playThis(props.track)"
    :class="[
      {
        currentInQueue: props.isCurrent,
      },
      { contexton: context_on },
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
        class="now-playing-track-indicator image"
        v-if="props.isCurrent"
        :class="{ last_played: !props.isPlaying }"
      ></div>
    </div>
    <div class="tags">
      <div class="title ellip cap-first">
       {{ props.track.title }}
      </div>
      <hr />
      <div class="artist ellip cap-first">
        <span v-for="artist in putCommas(props.track.artists)" :key="artist">{{
          artist
        }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ContextSrc } from "@/composables/enums";
import { putCommas } from "@/composables/perks";
import trackContext from "@/contexts/track_context";
import { Track } from "@/interfaces";

import { paths } from "@/config";
import useContextStore from "@/stores/context";
import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";

const contextStore = useContextStore();
const imguri = paths.images.thumb;

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
  (e: "PlayThis"): void;
}>();

const playThis = (track: Track) => {
  emit("PlayThis");
};
</script>

<style lang="scss">
.currentInQueue {
  background: linear-gradient(37deg, $gray4, $gray3, $gray3);
}

.contexton {
  background-color: $gray4;
  color: $white !important;
}

.track-item {
  display: grid;
  grid-template-columns: min-content 1fr;
  align-items: center;
  padding: $small 1rem;

  &:hover {
    cursor: pointer;
    background: linear-gradient(37deg, $gray4, $gray3, $gray3);
  }

  hr {
    border: none;
    margin: 0.1rem;
  }

  // .tags {
  //   border: solid 1px;
  // }

  .album-art {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 3rem;
    height: 3rem;
    margin: 0 0.5rem 0 0;
    background-image: url(../../assets/images/null.webp);
  }

  .title {
    word-break: break-all;
  }

  .artist {
    word-break: break-all;
    font-size: small;
    color: rgba(255, 255, 255, 0.637);
  }
}
</style>
