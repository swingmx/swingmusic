<template>
  <div class="albums-view rounded">
    <div class="al-header rounded">
      <div class="heading">ALL ALBUMS</div>
      <div class="search" >
        <input type="search" placeholder="Search albums">
      </div>
    </div>
    <div class="all-albums"></div>
  </div>
</template>
<script>
export default {
  setup() {
    const albums = [
      {
        title: "Album 1",
        artist: "Artist 1",
      },
      {
        title: "Album 2",
        artist: "Artist 2",
      },
      {
        title: "Album 3",
        artist: "Artist 3",
      },
    ];

    return {
      albums,
    };
  },
};
</script>

<style lang="scss">
.albums-view {
  height: calc(100% - 13rem);
  padding: $small;
  margin-top: $small;
  overflow: hidden;
  background-color: $card-dark;

  .al-header {
    display: flex;
    align-items: center;
    position: relative;
    background-color: rgb(48, 43, 43);
    // border: solid;
    height: 4em;
    // padding: $small;

    .search {
      position: absolute;
      right: 0;
    }
  }
}
</style>