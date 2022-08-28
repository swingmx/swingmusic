<template>
  <div class="right-search">
    <TabsWrapper>
      <Tab name="tracks">
        <TracksGrid :isOnSearchPage="isOnSearchPage" />
      </Tab>
      <Tab name="albums">
        <ArtistGrid :album_grid="true" />
      </Tab>
      <Tab name="artists">
        <ArtistGrid />
      </Tab>
    </TabsWrapper>
  </div>
</template>

<script setup lang="ts">
import ArtistGrid from "./ArtistGrid.vue";
import Tab from "./Tab.vue";
import TabsWrapper from "./TabsWrapper.vue";
import TracksGrid from "./TracksGrid.vue";

const props = defineProps<{
  isOnSearchPage?: boolean;
}>();
</script>

<style lang="scss">
.right-search {
  position: relative;
  overflow: hidden;
  height: 100%;
  width: 100%;

  .heading {
    padding: $medium;
    border-radius: $small;
    margin-bottom: $small;
    font-size: 2rem;
    color: $white;
  }

  .input {
    display: flex;
    align-items: center;
    position: relative;
  }
}
</style>
