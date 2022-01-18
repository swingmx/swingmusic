<template>
  <div class="r-tracks rounded border">
    <p class="heading">SIMILAR TRACKS</p>
    <div class="tracks">
      <div class="song-item" v-for="song in songs" :key="song">
        <div class="album-art image"></div>
        <div class="tags">
          <p class="title">{{ song.title }}</p>
          <hr />
          <p class="artist">{{ song.artist }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    const songs = [
      {
        title: "Mockingbird",
        artist: "Eminem",
      },
      {
        title: "Slim shady",
        artist: "Eminem",
      },
    ];

    const r_albums = ["Crybaby", "Everybody's Everything", "Castles II"];

    return { songs, r_albums };
  },
};
</script>

<style lang="scss">
.r-tracks {
  margin-top: 0.5rem;
  background-color: $card-dark;
  padding: 0.5rem;
}

.r-tracks .tracks .song-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.r-tracks .tracks .song-item:hover {
  background-color: #3a39393d;
  cursor: pointer;
}

.r-tracks .tracks .song-item hr {
  border: none;
  margin: 0.1rem;
}

.r-tracks .tracks .song-item .album-art {
  width: 3rem;
  height: 3rem;
  background-color: #ccc;
  margin: 0 0.5rem 0 0;
  border-radius: 0.5rem;
  background-image: url(../../assets/images/null.webp);
}

.r-tracks .tracks .song-item .artist {
  font-size: small;
  color: rgba(255, 255, 255, 0.637);
  margin: 0;
}

.r-tracks .tracks .song-item .title {
  margin: 0;
}
</style>