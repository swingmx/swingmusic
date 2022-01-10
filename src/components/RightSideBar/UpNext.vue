<template>
  <div class="up-next">
    <p class="heading">
      COMING UP NEXT <span class="more" @click="collapse">SEE ALL</span>
    </p>
    <div class="main-item h-1" @click="playNext">
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
        :class="{ hr: is_expanded, v0x: !is_expanded, v1x: is_expanded }"
        class="all-items"
      >
        <div :class="{ v0: !is_expanded, v1: is_expanded }" class="scrollable">
          <div
            class="song-item h-1"
            v-for="song in queue"
            :key="song"
            @click="playThis(song)"
            :class="{
              currentInQueue: current._id.$oid == song._id.$oid,
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
                v-if="current._id.$oid == song._id.$oid"
                :class="{ active: is_playing, not_active: !is_playing }"
              ></div>
            </div>
            <div class="tags">
              <p class="title ellip">{{ song.title }}</p>
              <hr />
              <p class="artist ellip">
                <span v-for="artist in putCommas(song.artists)" :key="artist">{{
                  artist
                }}</span>
              </p>
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
  max-height: 0em;
  overflow: hidden;
  transition: max-height 0.5s ease;
}

.up-next .v0x {
  background-color: transparent !important;
  transition: all 0.5s ease;
}

.up-next .v1x {
  transition: all .5s ease;
  background-color: rgb(218, 72, 96);
}

.up-next .v1 {
  max-height: 21em;
  transition: max-height 0.5s ease;
  padding: $small;

  .currentInQueue {
    background-color: rgba(0, 125, 241, 0.562);
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
  margin: 0.5rem 0 1rem 0rem;
}

.up-next > p > span {
  position: absolute;
  right: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  user-select: none;
}

.up-next > p > span:hover {
  background: $blue;
  cursor: pointer;
}

.up-next .main-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 0.5rem;

  &:hover {
    background-color: $blue;
  }
}

.up-next .main-item .album-art {
  width: 4.5rem;
  height: 4.5rem;
  background-image: url(../../assets/images/null.webp);
  margin: 0 0.5rem 0 0;
  border-radius: 0.5rem;
}

.up-next .main-item .tags hr {
  border: none;
  margin: 0.3rem;
}

.up-next .main-item .tags .title {
  width: 20rem;
  margin: 0;
}

.up-next .main-item .tags .artist {
  width: 20rem;
  margin: 0;
  font-size: small;
}

.up-next .all-items {
  padding-top: $small;
  border-radius: 0.5rem;
  padding: $small;
}

.up-next .all-items .scrollable {
  overflow-y: auto;
  background-color: $card-dark;
  border-radius: 0.5rem;

  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

.up-next .all-items p {
  margin: 0;
}

.up-next .all-items .scrollable .song-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.up-next .all-items .scrollable .song-item:hover {
  cursor: pointer;
  background-color: $blue;
}

.up-next .all-items .scrollable .song-item hr {
  border: none;
  margin: 0.1rem;
}

.up-next .all-items .album-art {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 3rem;
  height: 3rem;
  margin: 0 0.5rem 0 0;
  border-radius: 0.5rem;
  background-image: url(../../assets/images/null.webp);
}

.up-next .all-items .song-item .artist {
  width: 20rem;
  font-size: small;
  color: rgba(255, 255, 255, 0.637);
}
</style>
