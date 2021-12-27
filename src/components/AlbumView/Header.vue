<template>
  <div class="a-header rounded">
    <div id="header-blur"></div>
    <div
      class="art rounded"
      :style="{
        backgroundImage: `url(&quot;${album_info.image}&quot;)`,
      }"
    ></div>
    <div class="info">
      <div class="top">
        <div class="title">{{ album_info.name }}</div>
        <div class="artist">{{ album_info.artist }}</div>
      </div>
      <div class="separator"></div>
      <div class="bottom">
        <div class="stats">
          {{ album_info.count }} Tracks • {{ album_info.duration }} • 2021
        </div>
        <div class="play rounded">
          <div class="icon"></div>
          <div>Play</div>
        </div>
      </div>
    </div>
    <div class="most-played">
      <div class="image rounded"></div>
      <div>
        <div class="title">Girl Of My Dreams</div>
        <div class="artist">Juice Wrld, Suga [BTS]</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["album_info"],
  setup() {},
};
</script>

<style lang="scss">
#header-blur {
  height: 100%;
  width: 100%;
  position: absolute;
  z-index: -1;
  left: 0;
  backdrop-filter: blur(20px);
}

.a-header {
  position: relative;
  height: 14rem;
  background: #232526;
  background: -webkit-linear-gradient(to right, #414345, #232526);
  background: linear-gradient(to right, #050107, #00090e);

  backdrop-filter: blur(0px);
  overflow: hidden;

  display: flex;
  align-items: center;
  padding: 0 1rem 0 1rem;

  .most-played {
    position: absolute;
    display: flex;
    align-items: center;
    padding: 0 0 0 $small;
    background-color: rgb(24, 24, 24);
    border-radius: 1rem;
    right: 1rem;
    width: 25rem;
    height: 5rem;

    .image {
      width: 4rem;
      height: 4rem;
      background-image: url(../../assets/images/jw.jpeg);
    }

    .title {
      margin-left: $small;
      margin-bottom: $small;
    }

    .artist {
      font-size: small;
      margin-left: $small;
    }
  }

  .art {
    width: 12rem;
    height: 12rem;
    background: no-repeat center/cover url(../../assets/images/null.webp);
    margin-right: 1rem;
  }

  .info {
    width: calc(100% - 13rem);
    height: calc(100% - 1rem);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .title {
        font-size: 2rem;
        font-weight: bold;
        color: white;
      }

      .artist {
        margin-top: $small;
        color: rgba(255, 255, 255, 0.856);
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      .stats {
        font-weight: bold;
      }
      .play {
        height: 2.5rem;
        width: 6rem;
        display: flex;
        align-items: center;
        background: $blue;
        padding: $small;
        margin: $small 0;

        .icon {
          height: 1.5rem;
          width: 1.5rem;
          margin-right: $small;
          background: url(../../assets/icons/play.svg) no-repeat center/cover;
        }
      }
    }
  }
}
</style>