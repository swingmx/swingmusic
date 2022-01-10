<template>
  <div class="now-playing">
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
      <div class="duration">{{ fmtMSS(current.length) }}</div>
      <input
        id="progress"
        type="range"
        :value="pos"
        min="0"
        max="1000"
        @change="seek()"
      />
    </div>
    <div class="controls">
      <div class="shuffle">
        <div class="image"></div>
        <div class="image"></div>
      </div>
      <div class="nav">
        <div class="image" id="previous" @click="playPrev"></div>
        <div
          class="image play-pause"
          @click="playPause"
          :class="{ isPlaying: isPlaying }"
        ></div>
        <div class="image" id="next" @click="playNext"></div>
      </div>
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
};
</script>

<style lang="scss">
.now-playing {
  border-radius: 0.5rem;
  height: 14rem;
  margin-top: .5rem;
  padding: 0.5rem;
  background: $card-dark;
  display: grid;
  grid-template-rows: 3fr 1fr;

  .progress {
    display: flex;
    align-items: center;
    height: 1.5rem;
    position: relative;

    .duration {
      position: absolute;
      right: 0;
      top: -1rem;
      font-size: small;
    }

    input {
      -webkit-appearance: none;
      width: 100%;
      border: none;
      outline: none;
      background: transparent;
    }

    input:focus {
      outline: none;
    }

    input::-webkit-slider-runnable-track {
      width: 100%;
      height: 0.25rem;
      cursor: pointer;
      background: #1488cc;
      background: linear-gradient(
        to right,
        #1488cc,
        #2b32b2
      );
    }

    input::-webkit-slider-thumb {
      -webkit-appearance: none;
      height: 1rem;
      width: 1rem;
      border-radius: 50%;
      background: #ffffff;
      cursor: pointer;
      margin-top: -0.35rem;
    }

    input:focus::-webkit-slider-runnable-track,
    input::-moz-range-track {
      background: #367ebd;
    }

    input::-moz-range-thumb {
      height: 1rem;
      width: 1rem;
      border-radius: 50%;
      background: #ffffff;
      cursor: pointer;
      margin-top: -0.35rem;
    }
  }

  .controls {
    display: grid;
    grid-template-columns: repeat(3, 1fr);

    .nav {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      width: 100%;

      & * {
        height: 3rem;
        width: 3rem;
        background-size: 50%;
        cursor: pointer;
        border-radius: 0.5rem;
      }

      #previous {
        background-image: url(../../assets/icons/previous.svg);
      }

      .play-pause {
        background-image: url(../../assets/icons/play.svg);
      }

      .isPlaying {
        background-image: url(../../assets/icons/pause.svg);
      }

      #next {
        background-image: url(../../assets/icons/next.svg);
      }
    }

    .shuffle {
      width: 100%;
      display: flex;
      align-items: center;

      & * {
        height: 2rem;
        width: 2rem;
        background-size: 70%;
        cursor: pointer;
        border-radius: 0.5rem;
      }

      & :first-child {
        background-image: url(../../assets/icons/repeat.svg);
      }

      & :last-child {
        background-image: url(../../assets/icons/shuffle.svg);
      }
    }

    .fav {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: flex-end;

      & * {
        height: 2rem;
        width: 2rem;
        background-size: 70%;
        border-radius: 0.5rem;
        cursor: pointer;
      }

      & :first-child {
        background-image: url(../../assets/icons/plus.svg);
      }

      & :last-child {
        background-image: url(../../assets/icons/heart.svg);
      }
    }

    .fav *:hover,
    .shuffle *:hover,
    .nav *:hover {
      background-color: rgb(5, 80, 150);
    }
  }

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
      background-color: #ad1717a8;
      background-image: url(../../assets/images/null.webp);
    }
  }
}
</style>