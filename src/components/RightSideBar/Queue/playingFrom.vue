<template>
  <div id="playing-from" class="bg-black rounded" @click="goTo">
    <div class="h">
      <div class="icon image" :class="from.icon"></div>
      Playing from
    </div>
    <div class="name cap-first">
      <div id="to">
        {{ from.text }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  fromFolder,
  fromAlbum,
  fromPlaylist,
  fromSearch,
} from "@/interfaces";
import { FromOptions } from "@/composables/enums";
import { useRouter } from "vue-router";
import { computed } from "@vue/reactivity";

const props = defineProps<{
  from: fromFolder | fromAlbum | fromPlaylist | fromSearch;
}>();

interface from {
  icon: string;
  text: string;
}

const from = computed((): from => {
  switch (props.from.type) {
    case undefined:
      return {
        icon: "album",
        text: "Welcome to Alice",
      };
    case FromOptions.folder:
      return {
        icon: "folder",
        text: props.from.name,
      };
    case FromOptions.album:
      return {
        icon: "album",
        text: `${props.from.name} - ${props.from.albumartist}`,
      };
    case FromOptions.playlist:
      return {
        icon: "playlist",
        text: props.from.name,
      };
    case FromOptions.search:
      return {
        icon: "search",
        text: `Search results for: "${props.from.query}"`,
      };
  }
});

const router = useRouter();

function goToAlbum(from: fromAlbum) {
  router.push({
    name: "AlbumView",
    params: {
      hash: from.hash,
    },
  });
}

function goToFolder(from: fromFolder) {
  router.push({
    name: "FolderView",
    params: {
      path: from.path,
    },
  });
}

function goToPlaylist(from: fromPlaylist) {
  router.push({
    name: "PlaylistView",
    params: {
      pid: from.playlistid,
    },
  });
}

function goTo() {
  switch (props.from.type) {
    case FromOptions.folder:
      goToFolder(props.from);
      break;
    case FromOptions.album:
      goToAlbum(props.from);
      break;
    case FromOptions.playlist:
      goToPlaylist(props.from);
      break;
  }
}
</script>

<style lang="scss">
#playing-from {
  background-size: 120%;
  padding: 0.75rem;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
  background-color: $black;

  &:hover {
    background-position: -4rem;
  }

  .name {
    font-weight: bolder;
  }

  .h {
    font-size: 0.9rem;
    margin-bottom: $small;
    display: flex;
    align-items: center;
    gap: $small;
    color: rgba(255, 255, 255, 0.849);

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
