<template>
  <div class="queue-view">
    <Layout :tracks="queue.tracklist" :no_header="true"> </Layout>
  </div>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";
import Layout from "@/layouts/HeaderAndVList.vue";

const queue = useQStore();
</script>
