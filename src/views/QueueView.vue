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
import { onBeforeMount, onMounted } from "vue";

const queue = useQStore();

function playFromQueue(index: number) {
  queue.play(index);
}

function scrollToCurrent() {
  const scrollable = document.getElementById("v-page-scrollable");
  const itemHeight = 64;
  const top = queue.currentindex * itemHeight - 290;

  scrollable?.scrollTo({
    top,
    behavior: "smooth",
  });
}

onBeforeMount(() => {
  setTimeout(() => {
    scrollToCurrent();
  }, 1000);
});
</script>
