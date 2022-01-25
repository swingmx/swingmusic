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
        <div
          class="song-item h-1"
          v-for="song in queue"
          :key="song"
          @click="playThis(song)"
          :class="{
            currentInQueue: current.id == song.id,
          }"
        >
          <div
            class="album-art image"
            :style="{
              backgroundImage: `url(&quot;${song.image}&quot;)`,
            }"
          >
            <div
              class="now-playing-track image"
              v-if="current.id == song.id"
              :class="{ active: is_playing, not_active: !is_playing }"
            ></div>
          </div>
          <div class="tags">
            <div class="title ellip">{{ song.title }}</div>
            <hr />
            <div class="artist ellip">
              <span v-for="artist in putCommas(song.artists)" :key="artist">{{
                artist
              }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, toRefs } from "@vue/reactivity";
import perks from "@/composables/perks.js";
import audio from "@/composables/playAudio.js";
import state from "@/composables/state.js";
import { watch } from "@vue/runtime-core";

export default {
  props: ["up_next"],
  setup(props, { emit }) {
    const is_expanded = toRefs(props).up_next;

    const queue = ref(perks.queue);
    const current = ref(perks.current);
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
    const { playAudio } = audio;

    const playThis = (song) => {
      playAudio(song.filepath);
      perks.current.value = song;
    };

    const putCommas = perks.putCommas;

    return {
      collapse,
      is_expanded,
      is_playing: state.is_playing,
      playNext,
      playThis,
      putCommas,
      queue,
      current,
      next,
    };
  },
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

.up-next .scrollable .song-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;

  &:hover {
    cursor: pointer;
    background-color: $blue;
  }

  hr {
    border: none;
    margin: 0.1rem;
  }

  .album-art {
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
    width: 20rem;
    font-size: small;
    color: rgba(255, 255, 255, 0.637);
  }
}
</style>
