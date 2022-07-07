<template>
    <Header :album="album" />
</template>

<script setup lang="ts">
import Header from "@/components/AlbumView/Header.vue";
import { AlbumInfo } from "@/interfaces";

defineProps<{
  album: AlbumInfo;
}>();
</script>
