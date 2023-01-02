<template>
  <div class="artist-page v-scroll-page" style="height: 100%">
    <DynamicScroller
      :items="scrollerItems"
      :min-item-size="64"
      class="scroller"
      style="height: 100%"
    >
      <template v-slot="{ item, index, active }">
        <DynamicScrollerItem
          :item="item"
          :active="active"
          :size-dependencies="[item.props]"
          :data-index="index"
        >
          <component
            :key="index"
            :is="item.component"
            v-bind="item.props"
          ></component>
        </DynamicScrollerItem>
      </template>
    </DynamicScroller>
  </div>
</template>

<script setup lang="ts">
import Header from "@/components/ArtistView/Header.vue";
import TopTracks from "@/components/ArtistView/TopTracks.vue";
import useArtistPageStore from "@/stores/pages/artist";
import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import ArtistAlbumsFetcher from "@/components/ArtistView/ArtistAlbumsFetcher.vue";
import { computed } from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from "vue-router";
import { Album } from "@/interfaces";
import { discographyAlbumTypes, FromOptions } from "@/composables/enums";
import useQueueStore from "@/stores/queue";
import { getArtistTracks } from "@/composables/fetch/artists";

const store = useArtistPageStore();
const queue = useQueueStore();
const route = useRoute();

interface ScrollerItem {
  id: string | number;
  component: any;
  props?: Record<string, unknown>;
}

const header: ScrollerItem = {
  id: "artist-header",
  component: Header,
};

const artist_albums_fetcher: ScrollerItem = {
  id: "artist-albums-fetcher",
  component: ArtistAlbumsFetcher,
};

enum AlbumType {
  ALBUMS = "Albums",
  EPS = "EPs",
  SINGLES = "Singles",
  APPEARANCES = "Appearances",
}

function createAbumComponent(title: AlbumType, albums: Album[]) {
  let albumType = null;

  switch (title) {
    case AlbumType.ALBUMS:
      albumType = discographyAlbumTypes.albums;
      break;
    case AlbumType.EPS:
      albumType = discographyAlbumTypes.eps;
      break;
    case AlbumType.SINGLES:
      albumType = discographyAlbumTypes.singles;
      break;
    case AlbumType.APPEARANCES:
      albumType = discographyAlbumTypes.appearances;
      break;

    default:
      break;
  }
  return {
    id: title,
    component: ArtistAlbums,
    props: {
      albumType,
      albums,
      title,
      artisthash: route.params.hash,
      route: `/artists/${store.info.artisthash}/discography?artist=${store.info.name}`,
    },
  };
}

function getTopTracksComponent(): ScrollerItem {
  return {
    id: "artist-top-tracks",
    component: TopTracks,
    props: {
      tracks: store.tracks,
      title: "Tracks",
      route: `/artists/${store.info.artisthash}/tracks?artist=${store.info.name}`,
      playHandler: handlePlay,
    },
  };
}

const scrollerItems = computed(() => {
  let components = [header];

  if (store.tracks.length > 0) {
    components.push(getTopTracksComponent());
  }

  components = [...components, artist_albums_fetcher];

  if (store.albums.length > 0) {
    const albums = createAbumComponent(AlbumType.ALBUMS, store.albums);
    components.push(albums);
  }

  if (store.eps.length > 0) {
    const eps = createAbumComponent(AlbumType.EPS, store.eps);
    components.push(eps);
  }

  if (store.singles.length > 0) {
    const singles = createAbumComponent(AlbumType.SINGLES, store.singles);
    components.push(singles);
  }

  if (store.appearances.length > 0) {
    const appearances = createAbumComponent(
      AlbumType.APPEARANCES,
      store.appearances
    );
    components.push(appearances);
  }

  return components;
});

async function handlePlay(index: number) {
  if (
    queue.from.type == FromOptions.artist &&
    queue.from.artisthash == store.info.artisthash
  ) {
    queue.play(index);
    return;
  }

  const tracks = await getArtistTracks(store.info.artisthash);
  queue.playFromArtist(store.info.artisthash, store.info.name, tracks);
  queue.play(index);
}

onBeforeRouteUpdate(async (to) => {
  await store.getData(to.params.hash as string);
});

onBeforeRouteLeave(async () => {
  setTimeout(() => {
    store.resetAlbums();
  }, 400);
});
</script>

<style lang="scss">
.artist-page {
  .artist-albums {
    margin-top: 2rem;
  }

  .section-title {
    margin: 1rem;
    padding-left: 1rem;
  }
}
</style>
