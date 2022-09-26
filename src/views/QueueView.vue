<template>
  <div class="queue-view" style="height: 100%">
    <Layout
      :tracks="queue.tracklist"
      :no_header="true"
      @playFromPage="playFromQueue"
    >
    </Layout>
  </div>
</template>

<script setup lang="ts">
import useQStore from "@/stores/queue";
import Layout from "@/layouts/HeaderAndVList.vue";

const queue = useQStore();

function playFromQueue(index: number) {
  queue.play(index);
}
</script>
