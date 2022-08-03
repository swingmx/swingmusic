<template>
  <div class="right-search">
    <TabsWrapper>
      <Tab name="Top Results">
        <ArtistGrid />
      </Tab>
      <Tab name="tracks">
        <TracksGrid />
      </Tab>
      <Tab name="albums">
        <AlbumGrid />
      </Tab>
      <Tab name="artists">
        <ArtistGrid />
      </Tab>
      <Tab name="Playlists">
        <ArtistGrid />
      </Tab>
    </TabsWrapper>
  </div>
</template>

<script setup lang="ts">
import AlbumGrid from "./AlbumGrid.vue";
import ArtistGrid from "./ArtistGrid.vue";
import Tab from "./Tab.vue";
import TabsWrapper from "./TabsWrapper.vue";
import TracksGrid from "./TracksGrid.vue";
</script>

<style lang="scss">
.right-search {
  position: relative;
  overflow: hidden;
  width: auto;
  height: 100%;

  .heading {
    padding: $medium;
    border-radius: $small;
    margin-bottom: $small;
    font-size: 2rem;
    color: $white;
  }
  .search-results-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }

  .input {
    display: flex;
    align-items: center;
    position: relative;
  }
}
</style>
