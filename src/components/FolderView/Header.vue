<template>
  <div class="folder-top flex">
    <div class="fname">
      <button class="play image" @click="playFolder(first_song)">
        <div class="icon"></div>
        Play
      </button>
      <div class="text">
        <div class="icon image"></div>
        <div class="ellip">
          {{ path.split("/").splice(-1) + "" }}
        </div>
      </div>
    </div>
    <div class="search">
      <div class="loaderr">
        <Loader />
      </div>
      <input
        type="text"
        class="search-input border"
        placeholder="Search this folder"
        v-model="query"
      />
      <div class="search-icon image"></div>
    </div>
  </div>
</template>

<script>
import perks from "@/composables/perks.js";
import { watch } from "@vue/runtime-core";
import useDebouncedRef from "@/composables/useDebouncedRef.js";
import Loader from "../shared/Loader.vue";

export default {
  props: ["path", "first_song"],
  components: { Loader },
  setup(props, { emit }) {
    const query = useDebouncedRef("", 400);

    function playFolder(song) {
      perks.updateQueue(song, "folder");
    }

    watch(query, () => {
      emit("search", query.value);
    });

    return {
      playFolder,
      query,
    };
  },
};
</script>

<style lang="scss">
.folder-top {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid $separator;
  width: calc(100% - 0.5rem);
  padding-bottom: $small;
  height: 3rem;
}

.folder-top .search {
  width: 50%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  place-items: end;

  .loaderr {
    width: 2rem;
  }

  .search-input {
    max-width: 20rem;
    width: 100%;
    border-radius: 0.5rem;
    padding-left: 1rem;
    background-color: transparent;
    color: $white;
    font-size: 1rem;
    line-height: 2.2rem;
    outline: none;
  }
}

.folder-top .fname {
  width: 50%;
  display: flex;
  align-items: center;

  .play {
    height: 100%;
    width: 5em;
    background-color: rgb(5, 74, 131);
    padding-left: $small;
    margin-right: $small;

    .icon {
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/play.svg);
      background-size: 1.5rem;
      background-position: 10%;
      margin-right: $small;
    }
  }

  .text {
    position: relative;
    display: flex;
    align-items: center;

    border-radius: $small;
    background-color: rgb(24, 22, 22);
    padding: $small $small $small 2.25rem;

    .icon {
      position: absolute;
      left: $small;
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/folder.svg);
      margin-right: $small;
    }

    @include phone-only {
      display: none;
    }
  }
}
</style>
