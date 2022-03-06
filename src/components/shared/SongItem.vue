<template>
  <tr
    class="songlist-item"
    :class="{ current: current.trackid === song.trackid }"
    @dblclick="emitUpdate(song)"
  >
    <td class="index">{{ index }}</td>
    <td class="flex">
      <div
        class="album-art image"
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
    </td>
    <td class="song-artists">
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
    </td>
    <td class="song-album">
      <div
        class="album ellip"
        @click="emitLoadAlbum(song.album, song.albumartist)"
      >
        {{ song.album }}
      </div>
    </td>
    <td class="song-duration">{{ formatSeconds(song.length) }}</td>
  </tr>
</template>

<script>
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";

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
};
</script>

<style lang="scss">
.songlist-item {
  .index {
    color: grey;
    font-size: 0.8rem;
    text-align: center;
    width: 2rem;

    @include phone-only {
      display: none;
    }
  }

  @include phone-only {
    width: 100%;

    td {
      background-color: #14161a;
      border-radius: $small;
    }
  }

  .song-duration {
    font-size: 0.8rem;
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

  &:hover {
    * {
      color: #fff;
    }
    & {
      & td {
        background-color: #3131313b;
      }

      td:first-child {
        border-radius: $small 0 0 $small;
      }

      td:nth-child(2) {
        border-radius: 0;

        @include phone-only {
          border-radius: $small;
        }
      }

      td:nth-child(3) {
        @include tablet-portrait {
          border-radius: 0 $small $small 0 !important;
        }

        @include tablet-landscape {
          border-radius: 0;
        }
      }

      & > td:nth-child(4) {
        @include tablet-landscape {
          border-radius: 0 $small $small 0 !important;
        }
      }

      & td:last-child {
        border-radius: 0 $small $small 0;
      }
    }
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
}
</style>
