<template>
  <div
    class="track-item h-1"
    @click="playThis(props.track)"
    :class="{
      currentInQueue: current.id == props.track.id,
    }"
  >
    <div
      class="album-art image"
      :style="{
        backgroundImage: `url(&quot;${props.track.image}&quot;)`,
      }"
    >
      <div
        class="now-playing-track image"
        v-if="current.id == props.track.id"
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

const props = defineProps({
  track: Object,
});

const current = ref(perks.current);
const putCommas = perks.putCommas;
const is_playing = ref(playAudio.playing);

const playThis = (song) => {
  playAudio.playAudio(song.filepath);
  perks.current.value = song;
};

</script>

<style lang="scss">
.currentInQueue {
  border: solid 2px $pink;
}

.track-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  position: relative;
  height: 4rem;
  padding-left: 4rem;

  &:hover {
    cursor: pointer;
    background-color: $blue;
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
    border-radius: 0.5rem;
    background-image: url(../../assets/images/null.webp);
  }
  .artist {
    font-size: small;
    color: rgba(255, 255, 255, 0.637);
  }
}
</style>
