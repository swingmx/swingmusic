<template>
  <div class="now-playing bg-black shadow-lg">
    <div class="art-tags">
      <div class="duration">{{ formatSeconds(current.length) }}</div>
      <div
          :style="{
          backgroundImage: `url(&quot;${current.image}&quot;)`,
        }"
          class="album-art image bg-black"
      ></div>
      <div class="t-a">
        <p id="title" class="ellipsis">{{ current.title }}</p>
        <div class="separator no-bg-black"></div>
        <div v-if="current.artists[0] !== ''" id="artist" class="ellip">
          <span v-for="artist in putCommas(current.artists)" :key="artist">{{
              artist
            }}</span>
        </div>
        <div v-else id="artist">
          <span>{{ current.albumartist }}</span>
        </div>
        <div id="type">
          <span v-if="current.bitrate > 330"
          >FLAC • {{ current.bitrate }} Kbps</span
          >
          <span v-else>MP3 | {{ current.bitrate }} Kbps</span>
        </div>
      </div>
    </div>
    <div class="progress">
      <div class="prog">
        <Progress/>
      </div>
    </div>
    <div class="c-wrapper rounded">
      <div class="controls">
        <div class="shuffle">
          <div class="image"></div>
          <div class="image"></div>
        </div>
        <HotKeys/>
        <div class="fav">
          <div class="image"></div>
          <div class="image"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import playAudio from "@/composables/playAudio.js";
import {ref} from "@vue/reactivity";
import {putCommas, formatSeconds} from "../../composables/perks.js";
import HotKeys from "../shared/HotKeys.vue";
import Progress from "../shared/Progress.vue";

export default {
  setup() {
    const current = ref(perks.current);
    const putCommas = perks.putCommas;

    const {playNext} = playAudio;
    const {playPrev} = playAudio;
    const {playPause} = playAudio;
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
      seek,
      isPlaying,
      formatSeconds: perks.formatSeconds,
    };
  },
  components: {Progress, HotKeys},
};
</script>

<style lang="scss">
.now-playing {
  border-radius: 0.5rem;
  height: 13.5rem;
  padding: 0.5rem;
  // background: rgba(255, 255, 255, 0.055);
  display: grid;
  grid-template-rows: 3fr 1fr;

  .progress {
    display: flex;

    .prog {
      width: 100%;
      display: grid;
      align-items: center;
    }
  }

  .art-tags {
    display: flex;
    align-items: center;
    position: relative;

    .t-a {
      #title {
        margin: 0;
        width: 20rem;
        color: #fff;
      }

      #artist {
        font-size: 0.8rem;
        width: 20rem;
        color: $highlight-blue;
      }
    }

    .duration {
      position: absolute;
      bottom: $small;
      right: 0;
      font-size: 0.9rem;
    }

    #type {
      font-size: $medium;
      color: $red;
      padding: $smaller;
      border-radius: $smaller;
      position: absolute;
      bottom: 0.1rem;
      border: solid 1px $red;
    }

    .album-art {
      width: 7rem;
      height: 7rem;
      border-radius: 0.5rem;
      margin-right: 0.5rem;
      background-image: url("../../assets/images/null.webp");
    }
  }

  .c-wrapper {
    background-color: $bbb;
    height: 3.5rem;
    padding: 0 $small;
    display: grid;
    align-items: center;
  }
}
</style>
