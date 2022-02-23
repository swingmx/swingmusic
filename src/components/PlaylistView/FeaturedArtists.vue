<template>
  <div class="f-artists border">
    <div class="xcontrols">
      <div class="prev" @click="scrollLeft"></div>
      <div class="next" @click="scrollRight"></div>
    </div>
    <div class="artists" ref="artists_dom">
      <div class="xartist c1 image">
        <div class="blur"></div>
        <div class="s2"></div>
        <p>Featured Artists</p>
      </div>
      <ArtistCard v-for="artist in artists" :key="artist" :artist="artist"         :color="232452" />
    </div>
  </div>
</template>
<script>
import { ref } from "@vue/reactivity";
import ArtistCard from "@/components/shared/ArtistCard.vue";

export default {
  props: ["artists"],
  components: {
    ArtistCard
  },
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

    return {
      artists_dom,
      scrollLeft,
      scrollRight,
    };
  },
};
</script>

<style lang="scss">
.f-artists {
  position: relative;
  height: 15em;
  width: calc(100%);
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
    background-color: rgb(51, 51, 51);
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
  gap: $small;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}

.f-artists .c1 {
  position: relative;
  background-size: 400px 11rem;
  background-position: 100%;
  width: 8.25rem;
  background-image: linear-gradient(
    320deg,
    #b63939 13%,
    #232452 50%,
    #232452 100%
  );

  transition: all 0.5s ease-in-out;

  &:hover {
    background-position: 0;
  }

  p {
    margin-left: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    text-shadow: 0 0 80px rgb(0, 0, 0);
  }
}
</style>