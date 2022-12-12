<template>
  <div
    style="width: fit-content"
    v-tooltip
    class="artistname ellip"
    :style="{
      width: 'fit-content',
      fontSize: small ? '0.85rem' : smaller ? 'small' : '',
    }"
    @click.stop="() => {}"
  >
    <div v-if="artists === null || artists.length === 0">
      <span>{{ albumartists }}</span>
    </div>
    <div v-else>
      <template v-for="(artist, index) in artists" :key="artist.artisthash">
        <RouterLink
          class="artist"
          :to="{
            name: Routes.artist,
            params: { hash: artist.artisthash },
          }"
          >{{ `${artist.name}` }}</RouterLink
        >
        {{ index === artists.length - 1 ? "" : ",&nbsp;" }}
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Artist } from "@/interfaces";
import { Routes } from "@/router/routes";

const props = defineProps<{
  artists: Artist[] | null;
  albumartists: Artist[] | string | null;
  small?: boolean;
  smaller?: boolean;
}>();
</script>

<style lang="scss">
.artistname {
  a {
    color: inherit;
    cursor: pointer !important;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
