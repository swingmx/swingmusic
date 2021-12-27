<template>
  <div class="f-a-artists">
    <div class="xcontrols">
      <div class="prev" @click="scrollLeftX"></div>
      <div class="next" @click="scrollRightX"></div>
    </div>
    <div class="artists" ref="artists_dom" v-on:mouseover="say">
      <div class="artist c1">
        <div class="blur"></div>
        <div class="s2"></div>
        <p>From The Same Artists</p>
      </div>
      <div class="artist" v-for="album in albums" :key="album">
        <div>
          <div class="artist-image rounded"></div>
          <p class="artist-name ellipsis">{{ album }}</p>
          <div class="a-circle"></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from "@vue/reactivity";

export default {
  setup() {
    const albums = [
      "Michael John Montgomery",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "11",
    ];

    const artists_dom = ref(null);

    const scrollLeftX = () => {
      const dom = artists_dom.value;
      dom.scrollBy({
        left: -700,
        behavior: "smooth",
      });
    };

    const scrollRightX = () => {
      const dom = artists_dom.value;
      dom.scrollBy({
        left: 700,
        behavior: "smooth",
      });
    };

    const scroll = (e) => {
      artists_dom.value.scrollBy({
        left: e.deltaY < 0 ? -700 : 700,
        behavior: "smooth",
      });
    };

    const say = () => {
      artists_dom.value.addEventListener("wheel", (e) => {
        e.preventDefault();
        scroll(e);
      });
    };

    return {
      albums,
      artists_dom,
      say,
      scrollLeftX,
      scrollRightX,
    };
  },
};
</script>

<style lang="scss">
.f-a-artists {
  position: relative;
  height: 14em;
  width: calc(100%);
  background-color: #1f1e1d;
  padding: $small;
  border-radius: $small;
  user-select: none;
}

.f-a-artists .xcontrols {
  z-index: 1;
  width: 5rem;
  height: 2rem;
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  justify-content: space-between;

  &:hover {
    z-index: 1;
  }

  .next {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
  }

  .prev {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
    transform: rotate(180deg);
  }
  .next,
  .prev {
    width: 2em;
    height: 2em;
    background-color: rgb(79, 80, 80);
    border-radius: $small;
    cursor: pointer;
    transition: all 0.5s ease;
  }

  .next:hover,
  .prev:hover {
    background-color: rgb(3, 1, 1);
    transition: all 0.5s ease;
  }
}

.f-a-artists .artists {
  position: absolute;
  bottom: 1em;
  width: calc(100% - 1em);
  height: 13em;
  display: flex;
  align-items: flex-end;
  flex-wrap: nowrap;
  overflow-x: scroll;

  &::-webkit-scrollbar {
    display: none;
  }
}

.f-a-artists .artist {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;
  margin-left: $smaller;
  margin-right: $smaller;
  width: 9em;
  height: 10em;
  border-radius: $small;
  background-color: #064e92;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
  cursor: pointer;

  .artist-image {
    width: 7em;
    height: 7em;
    margin-left: 0.5em;
    margin-bottom: $small;
    background: no-repeat center/cover url(../../assets/images/girl4.jpg);
  }

  .artist-name {
    margin: 0;
    text-align: center;
    font-size: small;
    width: 10em;
  }
  &:hover {
    transform: translateY(-0.5em);
    transition: all 0.5s ease-in-out;
  }
}

.f-a-artists .c1 {
  position: relative;
  background: rgb(145, 42, 56);
  width: 15em;
  overflow: hidden;
  margin-left: -0.1rem;

  background: linear-gradient(239deg, #704bca, #d77422, #064e92, #9cb0c3);
  background-size: 800% 800%;

  -webkit-animation: similarAlbums 29s ease infinite;
  -moz-animation: similarAlbums 29s ease infinite;
  -o-animation: similarAlbums 29s ease infinite;
  animation: similarAlbums 29s ease infinite;

  &:hover > .s2 {
    transition: all 0.5s ease;
    background: rgba(53, 53, 146, 0.8);
    width: 12em;
    height: 12em;
  }

  p {
    position: absolute;
    bottom: -2rem;
    margin-left: 0.5rem;
    z-index: 1;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
  }

  .blur {
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    -moz-backdrop-filter: blur(40px);
    border-radius: $small;
  }

  .s2 {
    position: absolute;
    display: n;
    right: -3em;
    bottom: -3em;
    width: 10em;
    height: 10em;
    background: rgba(53, 53, 146, 0.445);
    border-radius: 50%;
    transition: all 0.5s ease;
  }
}
</style>