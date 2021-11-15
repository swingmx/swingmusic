<template>
  <div class="home">
    <AlbumOfTheDay />
  </div>
</template>

<script>
import AlbumOfTheDay from "@/components/AlbumOfTheDay.vue";

export default {
  name: "Home",
  components: {
    AlbumOfTheDay,
  },
};
</script>
