<template>
  <div class="folder-top flex">
    <div class="fname">
      <button class="play image" @click="playThis(first_song)">
        <div class="icon"></div>
        Play
      </button>
      <div class="ellip text">
        <div class="icon image"></div>
        {{ path.split("/").splice(-1) + "" }}
      </div>
    </div>
    <div class="search">
      <input
        type="text"
        class="search-input"
        placeholder="Ctrl + F"
        v-model="search_query"
        @keyup.enter="search()"
      />
      <div class="search-icon image"></div>
    </div>
  </div>
</template>

<script>
import perks from "@/composables/perks.js";

export default {
  props: ["path", "first_song"],
  setup() {
    return {
      playThis: perks.updateQueue,
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
  place-items: end;

  .search-input {
    max-width: 20rem;
    width: 100%;
    border: 1px solid $separator;
    border-radius: .5rem;
    padding-left: 1rem;
    background-color: #46454500;
    color: #fff;
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
    border-radius: $small;
    display: flex;
    align-items: center;
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
    display: flex;
    align-items: center;

    border-radius: $small;
    background-color: rgb(24, 22, 22);
    padding: $small;

    .icon {
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/folder.svg);
      margin-right: $small;
    }
  }
}
</style>