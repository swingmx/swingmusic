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
        <p class="title">{{ next.title }}</p>
        <hr />
        <p class="artist">
          <span v-for="artist in putCommas(next.artists)" :key="artist">{{
            artist
          }}</span>
        </p>
      </div>
    </div>
    <div>
      <div :class="{ hr: is_expanded }" class="all-items">
        <div :class="{ v0: !is_expanded, v1: is_expanded }" class="scrollable">
          <div class="song-item h-1" v-for="song in queue" :key="song" @click="playThis(song)">
            <div
              class="album-art image"
              :style="{
                backgroundImage: `url(&quot;${song.image}&quot;)`,
              }"
            ></div>
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

export default {
  props: ["up_next"],
  setup(props, { emit }) {
    const is_expanded = toRefs(props).up_next;
    let collapse = () => {
      emit("expandQueue");
    };

    const { playNext } = audio;
    const {playAudio} = audio;

    const playThis = (song) => {
      playAudio(song.filepath);
      perks.current.value = song;
    }

    const queue = ref(perks.queue);
    const next = ref(perks.next);

    const putCommas = perks.putCommas;

    return { collapse, is_expanded, playNext, playThis, putCommas, queue, next };
  },
};
</script>

<style lang="scss">
.up-next .hr {
  border-top: 1px solid var(--separator);
}
.up-next .v0 {
  max-height: 0em;
  overflow: hidden;
  transition: max-height 0.5s ease;
}

.up-next .v1 {
  max-height: 20em;
  transition: max-height 0.5s ease;
}

.up-next {
  padding: 0.5rem;
  margin-top: 1rem;
  background-color: #131313b2;
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
  background: rgb(62, 69, 77);
  cursor: pointer;
}

.up-next .main-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
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
  color: rgba(255, 255, 255, 0.61);
}

.up-next .all-items {
  padding-top: $small;
}

.up-next .all-items .scrollable {
  height: 20rem;
  overflow-y: auto;
  background-color: rgba(2, 6, 14, 0.425);
  border-radius: 0.5rem;
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
}

.up-next .all-items .scrollable .song-item hr {
  border: none;
  margin: 0.1rem;
}

.up-next .all-items .album-art {
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
