<template>
  <tr
    class="songlist-item"
    :class="{ current: current._id.$oid == song._id.$oid }"
  >
    <td class="flex" @click="emitUpdate(song)">
      <div
        class="album-art rounded image"
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
      <div>
        <span class="ellip">{{ song.title }}</span>
        <div class="separator no-border"></div>
        <div class="artist ellip">
          <span v-for="artist in putCommas(song.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
      </div>
    </td>
    <td class="song-artists">
      <div class="ellip" v-if="song.artists[0] != ''">
        <span
          class="artist"
          v-for="artist in putCommas(song.artists)"
          :key="artist"
          >{{ artist }}</span
        >
      </div>
      <div class="ellip" v-else>
        <span class="artist">{{ song.album_artist }}</span>
      </div>
    </td>
    <td class="song-album">
      <div class="ellip" @click="emitLoadAlbum(song.album, song.album_artist)">
        {{ song.album }}
      </div>
    </td>
    <td class="song-duration">
      {{ `${Math.trunc(song.length / 60)} min` }}
    </td>
  </tr>
</template>

<script>
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";

export default {
  props: ["song"],
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
    };
  },
};
</script>

<style lang="scss">
.songlist-item {
  @include phone-only {
    border: solid;

    td {
      background-color: $card-dark;
      border: 1px solid rgba(255, 255, 255, 0.096);
      border-radius: $small;
    }
  }

  cursor: pointer;

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
    }

    .artist {
      display: none;
      font-size: 0.8rem;
      color: rgba(255, 255, 255, 0.719);

      @include phone-only {
        display: unset;
      }
    }
  }

  td {
    height: 4rem;
    padding: $small;
  }

  &:hover {
    & {
      & td {
        background-color: rgb(5, 80, 150);
      }

      & td:first-child {
        border-radius: $small 0 0 $small;

        @include phone-only {
          border-radius: $small;
        }
      }

      td:nth-child(2) {
        @include tablet-portrait {
          border-radius: 0 $small $small 0 !important;
        }

        @include tablet-landscape {
          border-radius: 0;
        }
      }

      & > td:nth-child(3) {
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
    @include tablet-portrait {
      display: none;
    }
  }

  .song-artists {
    @include phone-only {
      display: none;
    }
  }
}
</style>