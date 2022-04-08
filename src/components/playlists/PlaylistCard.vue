<template>
  <router-link
    :to="{ name: 'PlaylistView', params: { pid: props.playlist.playlistid } }"
    :playlist="props.playlist"
    class="p-card rounded"
  >
    <div class="drop">
      <Option :color="'#48484a'" />
    </div>
    <div
      class="image p-image rounded shadow-sm"
      :style="{
        backgroundImage: `url(${props.playlist.image})`,
      }"
    ></div>
    <div class="pbtn">
      <PlayBtn />
    </div>
    <div class="bottom">
      <div class="name ellip">{{ props.playlist.name }}</div>
      <div class="count">
        <span v-if="props.playlist.count == 0">No Tracks</span>
        <span v-else-if="props.playlist.count == 1"
          >{{ props.playlist.count }} Track</span
        >
        <span v-else>{{ props.playlist.count }} Tracks</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { Playlist } from "../../interfaces";
import PlayBtn from "../shared/PlayBtn.vue";
import Option from "../shared/Option.vue";

const props = defineProps<{
  playlist: Playlist;
}>();

</script>

<style lang="scss">
.p-card {
  width: 100%;
  padding: 0.75rem;
  transition: all 0.2s ease;
  background-image: linear-gradient(37deg, #000000e8, $gray);
  position: relative;

  .p-image {
    min-width: 100%;
    height: 10rem;
    transition: all 0.2s ease;
  }

  .drop {
    position: absolute;
    bottom: 4rem;
    right: 1.25rem;
    opacity: 0;
    transition: all 0.25s ease-in-out;

    .drop-btn {
      background-color: $gray3;
    }
  }

  .pbtn {
    position: absolute;
    bottom: 4.5rem;
    left: 1.25rem;
    transition: all 0.25s ease-in-out;
    z-index: 10;
  }

  &:hover {
    .drop {
      transition-delay: .75s;
      opacity: 1;
      transform: translate(0, -.5rem);
    }
  }

  .bottom {
    margin-top: 1rem;

    .name {
      text-transform: capitalize;
    }

    .count {
      font-size: $medium;
      color: $gray1;
    }
  }
}
</style>
