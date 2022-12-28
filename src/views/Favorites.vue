<template>
  <div class="content-page favorites-page">
    <div class="header">
      <div class="tracks">Tracks</div>
      <div class="albums">Albums</div>
      <div class="artists">Artists</div>
      <div class="folders">Folders</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumSvg from "@/assets/icons/album.svg";
import ArtistSvg from "@/assets/icons/artist.svg";
import TrackSvg from "@/assets/icons/artist.svg";
</script>

<style lang="scss">
$tracksbg: rgb(55, 74, 243);
$albumsbg: rgb(255, 123, 0);
$artistsbg: rgb(0, 255, 21);

.favorites-page {
  height: 100%;
  overflow: scroll;

  .header > * {
    padding: 1rem;
    display: grid;
    place-content: center;
    border-radius: $small;
    font-weight: bold;
    width: 10rem;
  }

  .header {
    width: 100%;
    display: flex;
    gap: 1rem;

    .albums {
      background: $orange;
    }

    .tracks {
      background-color: $pink;
    }

    .artists {
      background-color: $blue;
    }

    .folders {
      background-color: $gray2;
    }
  }
}
</style>
