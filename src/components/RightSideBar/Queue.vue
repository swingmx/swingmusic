<template>
  <div class="up-next border">
    <p class="heading">COMING UP NEXT</p>
    <div class="r-grid">
      <div class="main-item h-1 border" @click="playNext">
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
        <div class="scrollable-r border rounded">
          <TrackItem v-for="song in queue" :key="song.track_id" :track="song" />
        </div>
    </div>
  </div>
</template>

<script>
import perks from "@/composables/perks.js";
import audio from "@/composables/playAudio.js";
import { ref, toRefs } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";
import TrackItem from "../shared/TrackItem.vue";

export default {
  props: ["up_next"],
  setup(props, { emit }) {
    const is_expanded = toRefs(props).up_next;
    const queue = ref(perks.queue);
    const next = ref(perks.next);

    let collapse = () => {
      emit("expandQueue");
    };

    watch(is_expanded, (newVal) => {
      if (newVal) {
        setTimeout(() => {
          perks.focusCurrent();
        }, 1000);
      }
    });

    const { playNext } = audio;

    const putCommas = perks.putCommas;
    return {
      collapse,
      is_expanded,
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
  background-color: $card-dark;
  padding: $small;
  overflow: hidden;
  height: 100%;

  .heading {
    position: relative;
    margin: 0.5rem 0 1rem 0;
  }

  .main-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    margin-bottom: 0.5rem;

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

    &:hover {
      background-color: $blue;
    }
  }

  .r-grid {
    position: relative;
    height: calc(100% - 2rem);
    display: grid;
    grid-template-rows: min-content;

    .scrollable-r {
      height: 100%;
      padding: $small;
      overflow: auto;
      background-color: $card-dark;
      scrollbar-color: grey transparent;

      &::-webkit-scrollbar-track {
        background-color: transparent;
      }
    }
  }
}
</style>
