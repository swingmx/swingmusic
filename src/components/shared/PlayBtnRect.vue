<template>
  <div class="playbtnrect rounded" @click="play">
    <div class="icon image"></div>
    <div class="text">Play</div>
  </div>
</template>

<script setup lang="ts">
import { playSources } from "../../composables/enums";

import useQStore from "../../stores/queue";
import useFStore from "../../stores/folder";
import useAStore from "../../stores/album";
import usePStore from "../../stores/p.ptracks";

const props = defineProps<{
  source: playSources;
}>();

const queue = useQStore();
const folder = useFStore();
const album = useAStore();
const playlist = usePStore();

function play() {
  switch (props.source) {
    // check which route the play request come from
    case playSources.folder:
      queue.playFromFolder(folder.path, folder.tracks);
      queue.play(queue.tracks[0]);
      break;
    case playSources.album:
      queue.playFromAlbum(album.info.album, album.info.artist, album.tracks);
      queue.play(album.tracks[0]);
      break;
    case playSources.playlist:
      queue.playFromPlaylist(
        playlist.playlist.name,
        playlist.playlist.playlistid,
        playlist.playlist.tracks
      );
      queue.play(playlist.playlist.tracks[0]);
      break;
  }
}
</script>

<style lang="scss">
.playbtnrect {
  width: 6rem;
  display: flex;
  align-items: center;
  height: 2.5rem;
  padding-left: 0.75rem;
  cursor: pointer;
  background: linear-gradient(
    34deg,
    rgba(255, 166, 0, 0.644) 30%,
    rgb(214, 188, 38)
  );
  user-select: none;
  transition: all 0.5s ease;

  .icon {
    height: 2rem;
    width: 2rem;
    background-image: url("../../assets/icons/play.svg");
  }

  &:hover {
    .icon {
      transform: rotate(120deg);
    }
  }
}
</style>
