<template>
  <div class="now-playing border">
    <div class="art-tags">
      <div
        class="album-art image"
        :style="{
          backgroundImage: `url(&quot;${current.image}&quot;)`,
        }"
      ></div>
      <div>
        <p id="title" class="ellipsis">{{ current.title }}</p>
        <hr />
        <div id="artist" class="ellip" v-if="current.artists[0] != ''">
          <span v-for="artist in putCommas(current.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
        <div id="artist" v-else>
          <span>{{ current.album_artist }}</span>
        </div>
      </div>
    </div>
    <div class="progress">
      <div class="duration">{{ current.length }}</div>
      <Progress />
    </div>
    <div class="controls">
      <div class="shuffle">
        <div class="image"></div>
        <div class="image"></div>
      </div>
      <HotKeys />
      <div class="fav">
        <div class="image"></div>
        <div class="image"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";

import perks from "../../composables/perks.js";
import playAudio from "@/composables/playAudio.js";

import Progress from "../shared/Progress.vue";
import HotKeys from "../shared/HotKeys.vue";

export default {
  setup() {
    const current = ref(perks.current);
    const putCommas = perks.putCommas;
    const pos = playAudio.pos;
    function fmtMSS(s) {
      return (s - (s %= 60)) / 60 + (9 < s ? ":" : ":0") + s;
    }
    const { playNext } = playAudio;
    const { playPrev } = playAudio;
    const { playPause } = playAudio;
    const isPlaying = playAudio.playing;
    const seek = () => {
      playAudio.seek(document.getElementById("progress").value);
    };
    return {
      current,
      putCommas,
      playNext,
      playPrev,
      playPause,
      pos,
      seek,
      isPlaying,
      fmtMSS,
    };
  },
  components: { Progress, HotKeys },
};
</script>

<style lang="scss">
.now-playing {
  border-radius: 0.5rem;
  height: 14rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: $card-dark;
  display: grid;
  grid-template-rows: 3fr 1fr;

  .art-tags {
    display: flex;
    align-items: center;

    hr {
      border: none;
      margin: 0.3rem;
    }

    #title {
      margin: 0;
      width: 22rem;
      color: #fff;
    }

    #artist {
      font-size: small;
      width: 22rem;
      color: rgba(255, 255, 255, 0.712);
    }

    .album-art {
      width: 6rem;
      height: 6rem;
      border-radius: 0.5rem;
      margin-right: 0.5rem;
      margin-left: $small;
      // background-color: #ad1717a8;
      background-image: url("../../assets/images/null.webp");
    }
  }
}
</style>
