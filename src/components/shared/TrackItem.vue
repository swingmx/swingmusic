<template>
  <div
    class="track-item h-1"
    @click="playThis(props.track)"
    :class="[
      {
        currentInQueue: current.trackid === props.track.trackid,
      },
      { 'context-on': context_on },
    ]"
    @contextmenu="showContextMenu"
  >
    <div
      class="album-art image rounded"
      :style="{
        backgroundImage: `url(&quot;${props.track.image}&quot;)`,
      }"
    >
      <div
        class="now-playing-track image"
        v-if="current.trackid === props.track.trackid"
        :class="{ active: is_playing, not_active: !is_playing }"
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

<script setup>
import { ref } from "vue";
import perks from "../../composables/perks";
import playAudio from "../../composables/playAudio";
import useContextStore from "@/stores/context.js";
import trackContext from "../../composables/track_context";

const contextStore = useContextStore();
const context_on = ref(false);

const showContextMenu = (e) => {
  e.preventDefault();
  e.stopPropagation();

  contextStore.showContextMenu(e, trackContext(props.track));
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
    }
  });
};
const props = defineProps({
  track: Object,
  default: () => ({}),
});

const current = ref(perks.current);
const putCommas = perks.putCommas;
const is_playing = ref(playAudio.playing);

const playThis = (song) => {
  playAudio.playAudio(song.trackid);
  perks.current.value = song;
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
  width: 26.55rem;
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
