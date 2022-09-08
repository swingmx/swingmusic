<template>
  <Page>
    <template #header>
      <Header :info="playlist" />
    </template>
    <template #content>
      <Content
        :tracks="tracks"
        :count="playlist.count"
        :name="playlist.name"
        :playlistid="playlist.playlistid"
      />
    </template>
  </Page>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import Page from "@/layouts/HeaderContentBottom.vue";

import Header from "@/components/PlaylistView/Header.vue";
import Content from "./Content.vue";

import usePlaylistStore from "@/stores/pages/playlist";
import { onBeforeRouteLeave } from "vue-router";

const store = usePlaylistStore();
const { info: playlist, tracks } = storeToRefs(store);

onBeforeRouteLeave(() => {
  setTimeout(() => {
    store.resetQuery();
  }, 500);
});
</script>

<style lang="scss"></style>
