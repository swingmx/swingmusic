<template>
  <div class="up-next border">
    <p class="heading">
      COMING UP NEXT <span class="more" @click="collapse">SEE ALL</span>
    </p>
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
    <div>
      <div
        :class="{ v0: !is_expanded, v1: is_expanded }"
        class="scrollable border"
      >
        <TrackItem v-for="song in queue" :key="song" :track="song" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";
import perks from "@/composables/perks.js";
import audio from "@/composables/playAudio.js";
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
.up-next .v0 {
  max-height: 0;
  transition: max-height 0.5s ease;
  visibility: hidden;
  padding: 0;
}

.up-next .v1 {
  max-height: 21em;
  transition: max-height 0.5s ease;
  padding: $small;

  .currentInQueue {
    border: 2px solid $pink;

    &:hover {
      color: #fff;
    }
  }
}

.up-next {
  padding: 0.5rem;
  margin-top: $small;
  background-color: $card-dark;
  border-radius: 0.5rem;
}

.up-next .heading {
  position: relative;
  margin: 0.5rem 0 1rem 0;

  span {
    position: absolute;
    right: 0.5rem;
    padding: 0.5rem;
    border-radius: 0.5rem;
    user-select: none;

    &:hover {
      background: $blue;
      cursor: pointer;
    }
  }
}

.up-next .main-item {
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

.up-next .scrollable {
  overflow-y: auto;
  background-color: $card-dark;
  border-radius: 0.5rem;

  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}
</style>
