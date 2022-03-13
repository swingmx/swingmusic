<template>
  <div
    class="songlist-item rounded"
    :class="{ current: current.trackid === song.trackid }"
    @dblclick="emitUpdate(song)"
  >
    <div class="index">{{ index }}</div>
    <div class="flex">
      <div
        class="album-art image rounded"
        :style="{ backgroundImage: `url(&quot;${song.image}&quot;` }"
        @click="emitUpdate(song)"
      >
        <div
          class="now-playing-track image"
          v-if="current.trackid === song.trackid"
          :class="{ active: is_playing, not_active: !is_playing }"
        ></div>
      </div>
      <div @click="emitUpdate(song)">
        <span class="ellip title">{{ song.title }}</span>
        <div class="artist ellip">
          <span v-for="artist in putCommas(song.artists)" :key="artist">
            {{ artist }}
          </span>
        </div>
      </div>
    </div>
    <div class="song-artists">
      <div class="ellip" v-if="song.artists[0] !== ''">
        <span
          class="artist"
          v-for="artist in putCommas(song.artists)"
          :key="artist"
          >{{ artist }}</span
        >
      </div>
      <div class="ellip" v-else>
        <span class="artist">{{ song.albumartist }}</span>
      </div>
    </div>
    <div class="song-album">
      <div
        class="album ellip"
        @click="emitLoadAlbum(song.album, song.albumartist)"
      >
        {{ song.album }}
      </div>
    </div>
    <div class="song-duration">{{ formatSeconds(song.length) }}</div>
    <ContextMenu />
  </div>
</template>

<script>
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";
import ContextMenu from "../contextMenu.vue";

export default {
  props: ["song", "index"],
  emits: ["updateQueue", "loadAlbum"],
  setup(props, { emit }) {
    function emitUpdate(song) {
      emit("updateQueue", song);
    }
    function emitLoadAlbum(title, artist) {
      emit("loadAlbum", title, artist);
    }
    return {
      putCommas: perks.putCommas,
      emitUpdate,
      emitLoadAlbum,
      is_playing: state.is_playing,
      current: state.current,
      formatSeconds: perks.formatSeconds,
    };
  },
  components: { ContextMenu },
};
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  align-items: center;
  grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr 0.25fr;
  height: 3.75rem;
  text-align: left;
  gap: $small;

  @include tablet-landscape {
    grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr;
  }

  @include tablet-portrait {
    grid-template-columns: 1.5rem 1.5fr 1fr;
  }

  &:hover {
    background-color: $gray;
  }

  .song-duration {
    @include tablet-landscape {
      display: none;
    }
  }

  .song-album {
    .album {
      cursor: pointer;
      max-width: max-content;
    }

    @include tablet-portrait {
      display: none;
    }
  }

  .song-artists {
    .artist {
      cursor: pointer;
    }

    @include phone-only {
      display: none;
    }
  }

  .index {
    color: grey;
    font-size: 0.8rem;
    text-align: center;
    width: 2rem;

    @include phone-only {
      display: none;
    }
  }

  .song-duration {
    font-size: 0.9rem;
    width: 5rem !important;
  }

  .flex {
    position: relative;
    padding-left: 4rem;
    align-items: center;

    .album-art {
      position: absolute;
      left: $small;
      width: 3rem;
      height: 3rem;
      margin-right: 1rem;
      display: grid;
      place-items: center;
      cursor: pointer;
    }

    .title {
      cursor: pointer;
    }

    .artist {
      display: none;
      font-size: 0.8rem;
      color: rgba(255, 255, 255, 0.719);
      cursor: pointer;

      @include phone-only {
        display: unset;
      }
    }
  }

  td {
    height: 4rem;
    padding: $small;
  }

  td:first-child {
    border-radius: $small 0 0 $small;
  }

  td:nth-child(2) {
    border-radius: 0 $small $small 0;

    @include phone-only {
      border-radius: $small;
    }
  }
}
</style>
