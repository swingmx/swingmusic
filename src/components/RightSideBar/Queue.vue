<template>
  <div class="up-next">
    <div class="r-grid">
      <div class="main-item  border" >
        <p class="heading">COMING UP NEXT</p>
        <div class="itemx" @click="playNext">
          <div
            class="album-art image"
            :style="{
              backgroundImage: `url(&quot;${next.image}&quot;)`,
            }"
          ></div>
          <div class="tags">
            <p class="title ellip">{{ next.title }}</p>
            <hr />
            <p class="artist ellip">
              <span v-for="artist in putCommas(next.artists)" :key="artist">{{
                artist
              }}</span>
            </p>
          </div>
        </div>
      </div>
      <div class="scrollable-r border rounded">
        <TrackItem v-for="song in queue" :key="song.trackid" :track="song" />
      </div>
    </div>
  </div>
</template>

<script>
import perks from "@/composables/perks.js";
import audio from "@/composables/playAudio.js";
import { ref } from "@vue/reactivity";
import TrackItem from "../shared/TrackItem.vue";

export default {
  setup() {
    const queue = ref(perks.queue);
    const next = ref(perks.next);

    const { playNext } = audio;

    const putCommas = perks.putCommas;

    return {
      playNext,
      putCommas,
      queue,
      next,
    };
  },
  components: { TrackItem },
};
</script>

<style lang="scss">
.up-next {
  padding: $small $small $small 0;
  overflow: hidden;
  height: 100%;

  .heading {
    position: relative;
    margin: 0.5rem 0 1rem 0;
  }

  .main-item {
    border-radius: 0.5rem;
    padding: 0.5rem;
    margin-bottom: 0.5rem;

    .itemx {
      display: flex;
      align-items: center;
      padding: 0.5rem;
      cursor: pointer;
      border-radius: 0.5rem;

      &:hover {
        background-color: $blue;
      }
    }

    .album-art {
      width: 4.5rem;
      height: 4.5rem;
      background-image: url(../../assets/images/null.webp);
      margin: 0 0.5rem 0 0;
      border-radius: 0.5rem;
    }

    .tags {
      hr {
        border: none;
        margin: 0.3rem;
      }
      .title {
        width: 20rem;
        margin: 0;
      }
      .artist {
        width: 20rem;
        margin: 0;
        font-size: small;
      }
    }
  }

  .r-grid {
    position: relative;
    height: 100%;
    display: grid;
    grid-template-rows: min-content;

    .scrollable-r {
      height: 100%;
      padding: $small;
      overflow: auto;
      // background-color: $card-dark;
      scrollbar-color: grey transparent;
    }
  }
}
</style>
