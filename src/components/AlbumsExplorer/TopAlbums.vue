<template>
  <div class="top-albums">
    <div class="heading">TOP ALBUMS</div>
    <div class="items">
      <router-link
        :to="{ path: '/albums/1' }"
        class="item rounded"
        v-for="album in albums"
        :key="album"
      >
        <div class="image rounded"></div>
        <div class="info">
          <div class="name ellip">{{ album.title }}</div>
          <div class="artist ellip">{{ album.artist }}</div>
          <div class="separator"></div>
          <div class="top">
            <div class="play-icon"></div>
            <div class="text ellip">{{ album.top_track }}</div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    const albums = [
      {
        title: "Thriller",
        artist: "Michael Jackson, Sting, Shaggy, Juice WRLD",
        top_track: "Beat It and althought you whatever",
      },
      {
        title: "Figting Demons",
        artist: "Juice WRLD",
        top_track: "Girl Of My Dreams",
      },
      {
        title: "Crybaby",
        artist: "Lil Peep",
        top_track: "Lil kennedy",
      },
    ];

    return {
      albums,
    };
  },
};
</script>

<style lang="scss">
.top-albums {
  height: 14rem;
  border-radius: $small;
  padding: $small;

  .heading {
    margin: $small 0 1.5em $small;
  }

  .items {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: $small;

    .item {
      height: 10rem;
      width: clamp(10rem, 100%, 25rem);
      background-color: rgb(7, 6, 6);
      display: grid;
      align-items: center;
      grid-template-columns: 7.5rem 1fr;
      padding: $small;
      cursor: pointer;
      transition: all 0.2s ease-in-out;

      &:hover {
        transform: translateY(-0.5em);
      }

      .image {
        height: 7rem;
        width: 7rem;
        background-image: url(../../assets/images/null.webp);
        border-radius: $small;
      }

      .info .name {
        font-size: 1.5rem;
        font-weight: bold;
      }

      .info .artist {
        font-size: small;
        color: rgba(255, 255, 255, 0.699);
      }

      .info .top {
        height: 2.5rem;
        background-color: $blue;
        border-radius: $small;
        margin-left: auto;
        display: grid;
        grid-template-columns: 2.5rem 1fr;
        align-items: center;
        transition: all 0.2s ease-in-out;
        user-select: none;

        .play-icon {
          margin: 0 0 0 $small;
          height: 1.2rem;
          width: 1.2rem;
          background-image: url(../../assets/icons/play.svg);
          background-size: 96%;
          background-repeat: no-repeat;
          background-position: center;
          transition: all 0.2s ease-in-out;
        }

        .text {
          color: white;
        }

        &:hover {
          background-color: rgb(0, 45, 104);
          transition: all 0.2s ease-in-out;

          .play-icon {
            transform: scale(1.2);
            transition: all 0.2s ease-in-out;
          }
        }

        &:active {
          transform: scale(0.95);
          transition: all 0.1s ease-in-out;
        }
      }
      &:first-child {
        background-color: rgb(177, 116, 2);

        .image {
          background-image: url(../../assets/images/null.webp);
        }
      }

      &:nth-child(2) {
        background-color: rgb(0, 74, 117);

        .image {
          background-image: url(../../assets/images/null.webp);
        }
      }

      &:nth-child(3) {
        background-color: rgb(161, 106, 106);
      }
    }
  }
}
</style>