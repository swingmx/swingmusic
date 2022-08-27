<template>
  <div class="sidebar-playlists">
    <div class="header">your playlists</div>
    <div class="list rounded">
      <div v-for="p in pStore.playlists" class="ellip">
        <router-link
          :to="{
            name: 'PlaylistView',
            params: {
              pid: p.playlistid,
            },
          }"
        >
          {{ p.name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import usePStore from "@/stores/pages/playlists";
import { onMounted } from "vue";
const pStore = usePStore();

onMounted(() => {
  if (pStore.playlists.length == 0) {
    pStore.fetchAll();
  }
});
</script>

<style lang="scss">
.sidebar-playlists {
  display: grid;
  grid-template-rows: max-content 1fr;

  .header {
    opacity: 0.5;
    margin-bottom: $small;
    margin-left: 1rem;
    font-size: small;
  }

  .list {
    padding: $small;

    & > * {
      padding: $small;
    }
  }
}
</style>
