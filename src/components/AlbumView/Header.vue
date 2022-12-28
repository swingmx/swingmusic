<template>
  <div
    class="album-header-ambient rounded"
    style="height: 100%; width: 100%"
    :style="{
      boxShadow: album.colors ? `0 .5rem 2rem ${album.colors[0]}` : '',
    }"
  ></div>
  <div
    class="a-header rounded"
    ref="albumheaderthing"
    :style="{
      backgroundColor: album.colors ? album.colors[0] : '',
    }"
  >
    <div
      class="big-img no-scroll"
      :class="`${albumHeaderSmall ? 'imgSmall' : ''} shadow-lg rounded-sm`"
    >
      <img :src="imguri.thumb.large + album.image" class="rounded-sm" />
    </div>
    <div
      class="info"
      :class="{ nocontrast: album.colors ? isLight(album.colors[0]) : false }"
    >
      <div class="album-info">
        <div class="top">
          <div v-auto-animate class="h">
            <span v-if="album.is_soundtrack">Soundtrack</span>
            <span v-else-if="album.is_compilation">Compilation</span>
            <span v-else-if="album.is_EP">EP</span>
            <span v-else-if="album.is_single">Single</span>
            <span v-else>Album</span>
          </div>
          <div class="title ellip2" v-tooltip>
            {{ album.title }}
          </div>
        </div>
        <div class="bottom">
          <div class="stats ellip">
            <div class="border rounded-sm pad-sm">
              <ArtistName
                :artists="album.albumartists"
                :albumartists="''"
                :small="true"
              />&nbsp; • {{ album.date }} • {{ album.count }}
              {{ album.count === 1 ? "Track" : "Tracks" }} •
              {{ formatSeconds(album.duration, true) }}
            </div>
          </div>
          <div class="buttons">
            <PlayBtnRect :source="playSources.album" :store="useAlbumStore" />
            <HeartSvg :state="album.is_favorite" @handleFav="handleFav" />
          </div>
        </div>
      </div>
      <div class="art" v-if="!albumHeaderSmall">
        <RouterLink
          v-for="a in album.albumartists"
          :to="{
            name: Routes.artist,
            params: { hash: a.artisthash },
          }"
        >
          <img
            :src="imguri.artist.small + a.image"
            class="shadow-lg circular"
            loading="lazy"
            :title="a.name"
            :style="{ border: `solid 2px ${album.colors[0]}` }"
          />
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import ArtistName from "@/components/shared/ArtistName.vue";
import { paths } from "@/config";
import { albumHeaderSmall } from "@/stores/content-width";
import useNavStore from "@/stores/nav";
import useAlbumStore from "@/stores/pages/album";
import { formatSeconds, useVisibility } from "@/utils";
import { isLight } from "@/composables/colors/album";
import { favType, playSources } from "@/composables/enums";
import { Album } from "@/interfaces";
import { Routes } from "@/router/routes";
import HeartSvg from "../shared/HeartSvg.vue";

import PlayBtnRect from "../shared/PlayBtnRect.vue";
import favoriteHandler from "@/composables/favoriteHandler";
import { storeToRefs } from "pinia";

// const props = defineProps<{
//   album: Album;
// }>();

const albumheaderthing = ref<any>(null);
const imguri = paths.images;
const nav = useNavStore();
const store = useAlbumStore();

const { info: album } = storeToRefs(store);

defineEmits<{
  (event: "playThis"): void;
}>();

/**
 * Calls the `toggleShowPlay` method which toggles the play button in the nav.
 * Emits the `resetBottomPadding` event to reset the album page content bottom padding.
 *
 * @param {boolean} state the new visibility state of the album page header.
 */
function handleVisibilityState(state: boolean) {
  nav.toggleShowPlay(state);
}

useVisibility(albumheaderthing, handleVisibilityState);

// const is_fav = ref(props.album.is_favorite);

function handleFav() {
  favoriteHandler(
    album.value.is_favorite,
    favType.album,
    album.value.albumhash,
    store.makeFavorite,
    store.removeFavorite
  );
}
</script>

<style lang="scss">
.album-header-ambient {
  width: 20rem;
  position: absolute;
  z-index: -100 !important;
  opacity: 0.25;
}

.a-header {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  height: $banner-height;
  background-color: $black;
  align-items: flex-end;

  .buttons {
    display: flex;
    gap: $small;
  }

  .big-img {
    height: calc(100%);
    width: 16rem;
    display: flex;
    align-items: flex-end;

    img {
      height: 16rem;
      aspect-ratio: 1;
    }
  }

  .big-img.imgSmall {
    width: 12rem;
    height: 12rem;

    img {
      height: 12rem;
    }
  }

  .nocontrast {
    color: $black;
  }

  .info {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr max-content;
    height: 100%;
    align-items: flex-end;

    .art {
      display: inline-flex;
      gap: $small;

      img {
        height: 3rem;
        background-color: $gray;
        border: solid 2px $white;
      }

      a {
        transition: all 0.25s ease-in-out;
      }

      a:hover {
        transform: scale(1.4);
      }
    }

    img {
      height: 6rem;
      aspect-ratio: 1;
      object-fit: cover;
      user-select: none;
    }

    .top {
      .h {
        font-size: 14px;
        opacity: 0.5;
      }

      .title {
        font-size: 2.5rem;
        font-weight: 600;
        width: fit-content;
        cursor: text;
      }

      .artist {
        font-size: 1.15rem;
        background-color: red;
      }
    }

    .bottom {
      margin-top: $smaller;

      .stats {
        font-weight: bold;
        margin-bottom: 0.75rem;
        font-size: 0.8rem;

        .artistname {
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        div {
          font-size: 0.8rem;
          display: flex;
          flex-wrap: wrap;
          // width: fit-content;
          // cursor: text;
        }
      }
    }
  }
}
</style>
