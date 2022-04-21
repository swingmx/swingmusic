<template>
  <div
    class="songlist-item rounded"
    :class="[{ current: props.isCurrent }, { 'context-on': context_on }]"
    @dblclick="emitUpdate(props.song)"
    @contextmenu="showContextMenu"
  >
    <div class="index">{{ props.index }}</div>
    <div class="flex">
      <div
        class="album-art image rounded"
        :style="{ backgroundImage: `url(&quot;${props.song.image}&quot;` }"
        @click="emitUpdate(props.song)"
      >
        <div
          class="now-playing-track image"
          v-if="props.isPlaying && props.isCurrent"
          :class="{ active: isPlaying, not_active: !isPlaying }"
        ></div>
      </div>
      <div @click="emitUpdate(props.song)">
        <span class="ellip title">{{ props.song.title }}</span>
      </div>
    </div>
    <div class="song-artists">
      <div class="ellip" v-if="props.song.artists[0] !== ''">
        <span
          class="artist"
          v-for="artist in perks.putCommas(props.song.artists)"
          :key="artist"
          >{{ artist }}</span
        >
      </div>
      <div class="ellip" v-else>
        <span class="artist">{{ props.song.albumartist }}</span>
      </div>
    </div>
    <router-link
      class="song-album"
      :to="{
        name: 'AlbumView',
        params: {
          album: props.song.album,
          artist: props.song.albumartist,
        },
      }"
    >
      <div class="album ellip">
        {{ props.song.album }}
      </div>
    </router-link>
    <div class="song-duration">
      {{ perks.formatSeconds(props.song.length) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import perks from "../../composables/perks.js";
import useContextStore from "../../stores/context";
import useModalStore from "../../stores/modal";
import { ContextSrc } from "../../composables/enums";

import { ref } from "vue";
import trackContext from "../../contexts/track_context";
import { Track } from "../../interfaces.js";

const contextStore = useContextStore();
const modalStore = useModalStore();
const context_on = ref(false);

const showContextMenu = (e: Event) => {
  e.preventDefault();
  e.stopPropagation();

  const menus = trackContext(props.song, modalStore);

  contextStore.showContextMenu(e, menus, ContextSrc.Track);
  context_on.value = true;

  contextStore.$subscribe((mutation, state) => {
    if (!state.visible) {
      context_on.value = false;
    }
  });
};

const props = defineProps<{
  song: Track;
  index: Number;
  isPlaying: Boolean;
  isCurrent: Boolean;
}>();

const emit = defineEmits<{
  (e: "updateQueue", song: Track): void;
}>();

function emitUpdate(track: Track) {
  emit("updateQueue", track);
}
</script>

<style lang="scss">
.songlist-item {
  display: grid;
  align-items: center;
  grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr 0.25fr;
  height: 3.75rem;
  text-align: left;
  gap: $small;

  .context {
    position: fixed;
    top: 0;
    left: 0;
    height: 45px;
    width: 45px;
    background-color: red;
  }
  @include tablet-landscape {
    grid-template-columns: 1.5rem 1.5fr 1fr 1.5fr;
  }

  @include tablet-portrait {
    grid-template-columns: 1.5rem 1.5fr 1fr;
  }

  &:hover {
    background-color: $gray4;
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
