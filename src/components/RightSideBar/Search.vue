<template>
  <div class="right-search">
    <TabsWrapper>
      <Tab name="tracks" v-motion-slide-visible-left>
        <TracksGrid />
      </Tab>
      <Tab name="albums">
        <AlbumGrid />
      </Tab>
      <Tab name="artists">
        <ArtistGrid />
      </Tab>
    </TabsWrapper>
  </div>
</template>

<script setup lang="ts">
import TabsWrapper from "./TabsWrapper.vue";
import Tab from "./Tab.vue";
import TracksGrid from "./Search/TracksGrid.vue";
import AlbumGrid from "./Search/AlbumGrid.vue";
import "@/assets/css/Search/Search.scss";
import ArtistGrid from "./Search/ArtistGrid.vue";
</script>

<style lang="scss">
.right-search {
  position: relative;
  overflow: hidden;
  width: auto;
  height: 100%;

  .no-res {
    text-align: center;
    display: grid;
    height: calc(100% - $small);
    place-items: center;
    font-size: 2rem;
    transition: all 0.3s ease;
    line-height: 4rem !important;

    .highlight {
      padding: $small;
      background-color: rgb(29, 26, 26);
    }
  }

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

.right-search .scrollable {
  overflow-y: auto;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>
