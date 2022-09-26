<template>
  <div class="now-playing-card t-center rounded">
    <SongCard :track="queue.currenttrack" />
  </div>
</template>

<script setup lang="ts">
import useQStore from "../../stores/queue";
import SongCard from "./NP/SongCard.vue";

const queue = useQStore();
</script>
<style lang="scss">
.now-playing-card {
  padding: 1rem;
}
</style>
