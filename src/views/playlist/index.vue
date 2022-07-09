<template>
  <Page>
    <template #header>
      <Header :info="playlist.info" />
    </template>
    <template #content>
      <Content
        :tracks="playlist.tracks"
        :count="playlist.info.count"
        :name="playlist.info.name"
        :playlistid="playlist.info.playlistid"
      />
    </template>
    <template #bottom>
      <FeaturedArtists :artists="playlist.artists" />
    </template>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/layouts/HeaderContentBottom.vue";

import Header from "@/components/PlaylistView/Header.vue";
import Content from "./Content.vue";
import FeaturedArtists from "@/components/PlaylistView/FeaturedArtists.vue";

import usePTrackStore from "@/stores/pages/playlist";
import { onBeforeUnmount, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const playlist = usePTrackStore();

onMounted(() => {
  playlist.fetchArtists(route.params.pid as string);
});
</script>

<style lang="scss"></style>
