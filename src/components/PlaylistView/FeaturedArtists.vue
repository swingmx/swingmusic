<template>
  <div class="f-artists">
    <div class="xcontrols">
      <div class="prev" @click="scrollLeftX"></div>
      <div class="next" @click="scrollRightX"></div>
    </div>
    <div class="artists" ref="artists_dom" v-on:mouseover="say">
      <div class="artist c1">
        <div class="blur"></div>
        <div class="s2"></div>
        <p>Featured Artists</p>
      </div>
      <div class="artist" v-for="artist in artists" :key="artist">
        <div>
          <div class="artist-image image"></div>
          <p class="artist-name ellipsis">{{ artist }}</p>
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
    const artists = [
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
      artists,
      artists_dom,
      say,
      scrollLeftX,
      scrollRightX,
    };
  },
};
</script>

<style lang="scss">
.f-artists {
  position: relative;
  height: 14em;
  width: calc(100% - 1em);
  background-color: #1f1e1d;
  padding: $small;
  border-radius: $small;
  user-select: none;
}

.f-artists .xcontrols {
  z-index: 1;
  width: 5rem;
  height: 2rem;
  position: absolute;
  top: 0.75rem;
  right: 0.5rem;
  display: flex;
  justify-content: space-between;

  .next,
  .prev {
    width: 2em;
    height: 2em;
    cursor: pointer;
    transition: all 0.5s ease;
  }

  .next {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
  }

  .prev {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
    transform: rotate(180deg);
  }

  .next:hover,
  .prev:hover {
    transform: scale(1.2);
    transition: all 0.5s ease;
  }

  .prev:hover {
    transform: rotate(180deg) scale(1.2);
  }

  .next:active {
    transform: scale(0.5);
  }

  .prev:active {
    transform: rotate(180deg) scale(0.5);
  }
}

.f-artists .heading {
  color: #fff;
  margin: 0 0 1em 1em;
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
  background-color: #fd5c63;
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
    transform: translateY(-1em);
    transition: all 0.5s ease-in-out;
  }
}

.f-artists .c1 {
  position: relative;
  background: rgb(145, 42, 56);
  width: 15em;
  background-image: url(../../assets/images/gradient1.gif);
  overflow: hidden;
  margin-left: -0.1rem;

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
    backdrop-filter: blur(100px);
    -webkit-backdrop-filter: blur(100px);
    -moz-backdrop-filter: blur(100px);
    border-radius: $small;
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