<template>
  <div class="albums-view rounded">
    <div class="al-header">
      <div class="heading">ALL ALBUMS</div>
      <div class="search">
        <input type="search" placeholder="Search albums" />
      </div>
    </div>
    <div class="separator"></div>
    <div class="all-albums">
      <router-link
        :to="{ path: '/albums/1' }"
        class="item rounded"
        v-for="album in albums"
        :key="album"
      >
        <div class="play"></div>
        <div class="album-art image rounded"></div>
        <div class="name ellip">{{ album.title }}</div>
        <div class="artist ellip">{{ album.albumartists }}</div>
      </router-link>
    </div>
  </div>
</template>
<script>
export default {
  setup() {
    const albums = [
      {
        title: "Album 2 af sjf s d kjf saf ",
        artist:
          "Artist  ad asd f adf d da df d adf ds d fadsf fs dfds sf dadf d",
      },
      {
        title: "Album 3",
        artist: "Artist 3",
      },
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
  height: calc(100% - 14.5rem);
  padding: $small;
  margin-top: $small;
  overflow: hidden;

  .all-albums {
    height: calc(100% - 4rem);
    padding: $small 0 0 0;
    overflow-y: auto;

    .item {
      position: relative;
      width: 10.9rem;
      height: 13rem;
      padding: $small 0.95rem $small 0.95rem;
      margin: $smaller;
      transition: all 0.2s ease-in-out;
      cursor: default;
      float: left;

      .play {
        position: absolute;
        bottom: 3rem;
        left: $small;
        height: 3rem;
        width: 3rem;
        background: url(../../assets/icons/play.svg) no-repeat center;
        background-size: 60%;
        cursor: default;
        opacity: 0;
        transition: all 0.5s ease-in-out;
      }

      &:hover {
        background-color: #574a4a;

        .play {
          transition: 0.5s all ease;
          opacity: 1;
        }
      }

      .album-art {
        height: 9em;
        width: 9em;
        background-image: url(../../assets/images/null.webp);
      }

      .name {
        text-align: left;
        font-weight: bold;
        margin-top: $small;
      }

      .artist {
        font-size: small;
        font-weight: lighter;
        text-align: left;
        color: rgba(255, 255, 255, 0.699);
      }
    }
  }

  .al-header {
    display: flex;
    align-items: center;
    position: relative;
    height: 4em;
    padding: 0 $small 0 $small;

    .search {
      position: absolute;
      right: 0;
      padding-right: $small;

      input {
        width: 30rem;
        border: none;
        border-radius: 2rem;
        padding-left: 1rem;
        background-color: #4645456c;
        color: rgba(255, 255, 255, 0.521);
        font-size: 1rem;
        line-height: 3rem;
        outline: none;
      }

      input::-webkit-search-cancel-button {
        position: relative;
        right: 20px;
        cursor: default;
        width: 50px;
        height: 50px;
      }
    }
  }
}
</style>