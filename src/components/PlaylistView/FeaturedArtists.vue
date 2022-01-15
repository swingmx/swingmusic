<template>
  <div class="f-artists">
    <div class="xcontrols">
      <div class="prev" @click="scrollLeft"></div>
      <div class="next" @click="scrollRight"></div>
    </div>
    <div class="artists" ref="artists_dom" v-on:mouseover="scrollArtists">
      <div class="artist c1">
        <div class="blur"></div>
        <div class="s2"></div>
        <p>Featured Artists</p>
      </div>
      <div class="artist" v-for="artist in artists" :key="artist">
        <div>
          <div
            class="artist-image image"
            :style="{ backgroundImage: `url('${artist.image}')` }"
          ></div>
          <p class="artist-name ellipsis">{{ artist.name }}</p>
          <div class="a-circle"></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from "@vue/reactivity";

export default {
  props: ["artists"],
  setup() {
    const artists_dom = ref(null);

    const scrollLeft = () => {
      const dom = artists_dom.value;
      dom.scrollBy({
        left: -700,
        behavior: "smooth",
      });
    };

    const scrollRight = () => {
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

    const scrollArtists = () => {
      artists_dom.value.addEventListener("wheel", (e) => {
        e.preventDefault();
        scroll(e);
      });
    };

    return {
      artists_dom,
      scrollArtists,
      scrollLeft,
      scrollRight,
    };
  },
};
</script>

<style lang="scss">
.f-artists {
  position: relative;
  height: 13em;
  width: calc(100%);
  background-color: $card-dark;
  padding: $small;
  border-radius: $small;
  user-select: none;
}

.f-artists .xcontrols {
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
    border-radius: $small;
    cursor: pointer;
    transition: all 0.5s ease;
    background-color: rgb(79, 80, 80);
  }

  .next:hover,
  .prev:hover {
    background-color: $blue;
    transition: all 0.5s ease;
  }
}

.f-artists .artists {
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

.f-artists .artist {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;
  margin-left: $smaller;
  margin-right: $smaller;
  width: 9em;
  height: 9em;
  border-radius: $small;
  background-color: #0f0e0e;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
  cursor: pointer;

  .artist-image {
    width: 7em;
    height: 7em;
    margin-left: 0.5em;
    border-radius: 50%;
    margin-bottom: $small;
    background: url(../../assets/images/girl1.jpg);
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
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

.f-artists .c1 {
  position: relative;
  background: rgb(16, 25, 51);
  width: 15em;

  &:hover > .s2 {
    background: rgba(53, 53, 146, 0.8);
    transition: all 0.5s ease;
    width: 12em;
    height: 12em;
  }

  p {
    position: absolute;
    bottom: -2rem;
    margin-left: 0.5rem;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
  }

  .s2 {
    position: absolute;
    left: -2em;
    bottom: -4em;
    width: 10em;
    height: 10em;
    background: rgba(53, 53, 146, 0.445);
    border-radius: 50%;
    transition: all 0.5s ease;
  }
}
</style>