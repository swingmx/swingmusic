<template>
  <div class="r-tracks rounded bg-primary">
    <div class="heading">Similar tracks</div>
    <div class="tracks">
      <div class="song-item" v-for="song in songs" :key="song.artist">
        <img src="" class="rounded" loading="lazy"/>
        <div class="tags">
          <div class="title">{{ song.title }}</div>
          <div class="artist">{{ song.artist }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const songs = [
  {
    title: "Imagine",
    artist: "John Lennon",
  },
  {
    title: "Mockingbird",
    artist: "Eminem",
  },
];
</script>

<style lang="scss">
.r-tracks {
  margin: 0.5rem 0 0.5rem 0;
  padding: 0.5rem;

  .heading {
    font-size: 1.25rem;
    margin-bottom: 0.5rem !important;
  }

  .tracks .song-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-radius: 0.5rem;

    img {
      width: 3rem;
      aspect-ratio: 1;
      margin-right: $small;
    }

    .title {
      margin: 0;
    }

    .artist {
      font-size: small;
      color: rgba(255, 255, 255, 0.637);
      margin: 0;
    }

    &:hover {
      background-color: #3a39393d;
    }
  }
}
</style>
