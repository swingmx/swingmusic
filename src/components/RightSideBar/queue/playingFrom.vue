<template>
  <div id="playing-from" class="rounded" @click="goTo">
  <div class="abs shadow-sm">Playing From</div>
    <div class="h">
      <div class="icon image" :class="from.type"></div>
      {{ from.type }}
    </div>
    <div class="name">
      <div id="to">
        {{ from.name }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { fromFolder, fromAlbum, fromPlaylist } from "../../../interfaces";
import { FromOptions } from "../../../composables/enums";
import { useRouter } from "vue-router";
import { computed } from "@vue/reactivity";

const props = defineProps<{
  from: fromFolder | fromAlbum | fromPlaylist;
}>();

interface from {
  type: string;
  name: string;
}

const from = computed((): from => {
  switch (props.from.type) {
    case undefined:
      return {
        type: "album",
        name: "Welcome to Alice",
      };
    case FromOptions.folder:
      return {
        type: "folder",
        name: props.from.name,
      };
    case FromOptions.album:
      return {
        type: "album",
        name: props.from.name,
      };
    case FromOptions.playlist:
      return {
        type: "playlist",
        name: props.from.name,
      };
  }
});

const router = useRouter();

function goToAlbum() {
  router.push({
    name: "AlbumView",
    params: {
      album: props.from.name,
      artist: props.from.albumartist,
    },
  });
}

function goToFolder() {
  router.push({
    name: "FolderView",
    params: {
      path: props.from.path,
    },
  });
}

function goToPlaylist() {
  router.push({
    name: "PlaylistView",
    params: {
      pid: props.from.playlistid,
    },
  });
}

function goTo() {
  switch (props.from.type) {
    case FromOptions.folder:
      goToFolder();
      break;
    case FromOptions.album:
      goToAlbum();
      break;
    case FromOptions.playlist:
      goToPlaylist();
      break;
  }
}
</script>

<style lang="scss">
#playing-from {
  background: linear-gradient(-200deg, $gray4 40%, $red, $gray4);
  background-size: 120%;
  padding: 0.75rem;
  margin-bottom: $small;
  cursor: pointer;
  position: relative;
  transition: all .2s ease;

  &:hover {
    background-position: -4rem;
  }

  .abs {
    position: absolute;
    right: $small;
    top: $small;
    font-size: .9rem;
    background-color: $gray;
    padding: $smaller;
    border-radius: .25rem;
  }

  .name {
    text-transform: capitalize;
    font-weight: bolder;
  }

  .h {
    font-size: .9rem;
    margin-bottom: $small;
    display: flex;
    align-items: center;
    gap: $small;
    text-transform: capitalize;
    color: rgba(255, 255, 255, 0.664);

    .icon {
      height: 1.25rem;
      width: 1.25rem;
    }

    .folder {
      background-image: url("../../../assets/icons/folder.fill.svg") !important;
    }

    .album {
      background-image: url("../../../assets/icons/album.svg") !important;
    }

    .playlist {
      background-image: url("../../../assets/icons/playlist.svg") !important;
    }
  }
}
</style>
