<template>
  <tr :class="{ current: current._id.$oid == song._id.$oid }">
    <td
      :style="{ width: songTitleWidth + 'px' }"
      class="flex"
      @click="emitUpdate(song)"
    >
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
      </div>
    </td>
    <td :style="{ width: songTitleWidth + 'px' }">
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
    <td :style="{ width: songTitleWidth + 'px' }">
      <div
        class="ellip"
       @click="emitLoadAlbum(song.album, song.album_artist)"
        >{{ song.album }}</div
      >
    </td>
    <td
      :style="{ width: songTitleWidth + 'px' }"
      v-if="songTitleWidth > minWidth"
    >
      {{ `${Math.trunc(song.length / 60)} min` }}
    </td>
  </tr>
</template>

<script>
import perks from "@/composables/perks.js";
import state from "@/composables/state.js";

export default {
  props: ["song", "songTitleWidth", "minWidth"],
  setup(props, { emit }) {
    function emitUpdate(song) {
      emit("updateQueue", song);
    }

    function emitLoadAlbum(title, artist){
      console.log(title, artist)
      emit("loadAlbum", title, artist)
    }

    return {
      putCommas: perks.putCommas,
      emitUpdate,
      emitLoadAlbum,
      is_playing: state.is_playing,
      current: state.current
    };
  },
};
</script>

<style>
</style>