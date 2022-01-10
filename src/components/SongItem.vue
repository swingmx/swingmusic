<template>
  <tr>
    <td
      :style="{ width: songTitleWidth + 'px' }"
      class="flex"
      @click="emitUpdate(song), playAudio(song.filepath)"
    >
      <div
        class="album-art rounded image"
        :style="{
          backgroundImage: `url(&quot;${song.image}&quot;)`,
        }"
      >
        <div
          class="now-playing-track image"
          v-if="current._id == song._id"
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
      <router-link
        class="ellip"
        :to="{
          name: 'AlbumView',
          params: { album: song.album, artist: song.album_artist },
        }"
        >{{ song.album }}</router-link
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
import audio from "@/composables/playAudio.js"

export default {
  props: ["song", "current", "songTitleWidth", "minWidth"],
  setup(props, { emit }) {
    function emitUpdate(song) {
      emit('updateQueue', song);
    }

    return {
      putCommas: perks.putCommas,
      emitUpdate,
      is_playing: state.is_playing,
      playAudio: audio.playAudio
    };
  },
};
</script>

<style>
</style>