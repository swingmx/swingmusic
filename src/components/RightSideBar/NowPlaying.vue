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
        <div id="artist">
          <span v-for="artist in putCommas(current.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
      </div>
    </div>
    <div class="progress">
      <input type="range" :value="pos" min="0" max="100" />
    </div>
    <div class="controls">
      <div class="shuffle">
        <div class="image"></div>
        <div class="image"></div>
      </div>
      <div class="nav">
        <div class="image" id="previous" @click="playPrev"></div>
        <div class="image" id="play-pause" @click="playPause"></div>
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

    const { playNext } = playAudio;
    const { playPrev } = playAudio;
    const { playPause } = playAudio;

    return { current, putCommas, playNext, playPrev, playPause, pos };
  },
};
</script>

<style lang="scss">
.now-playing {
  border-radius: 0.5rem;
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: rgb(12, 12, 12);
  display: grid;
  grid-template-rows: 3fr 1fr;

  .progress {
    display: flex;
    align-items: center;
    height: 1.5rem;

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
      background: #3071a9;
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

      & *:hover {
        filter: invert(66%) sepia(75%) saturate(4335%) hue-rotate(158deg)
          brightness(89%) contrast(101%);
      }

      #previous {
        background-image: url(../../assets/icons/previous.svg);
      }

      #play-pause {
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
      width: 13rem;
      color: #fff;
    }

    #artist {
      font-size: small;
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