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
import Page from "@/layouts/HeaderContentBottom.vue";

import Header from "@/components/PlaylistView/Header.vue";
import Content from "./Content.vue";

import usePTrackStore from "@/stores/pages/playlist";
import { onUnmounted } from "vue";

const { info: playlist, tracks } = usePTrackStore();
</script>

<style lang="scss"></style>
