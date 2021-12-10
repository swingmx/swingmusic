<template>
  <div class="f-artists">
    <div class="artists" ref="artists_dom" v-on:mouseover="say">
      <div class="artist c1">
        <div class="blur"></div>
        <div class="s2"></div>
        <p>Featured Artists</p>
      </div>
      <div class="artist" v-for="artist in artists" :key="artist">
        <div>
          <div class="artist-image image"></div>
          <p class="artist-name">{{ artist }}</p>
          <div class="a-circle"></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from '@vue/reactivity';

export default {
  setup() {
    const artists = [
      "Eminem",
      "Drake",
      "Kendrick Lamar",
      "Eminem",
      "Drake",
      "Kendrick Lamar",
      "Eminem",
      "Drake",
      "Kendrick Lamar",
      "Eminem",
      "Drake",
      "Kendrick Lamar",
      "Eminem",
      "Drake",
      "Kendrick Lamar",
    ];

    const artists_dom = ref(null)

    const say = () => {
      
    }

    return {
      artists,
      artists_dom,
      say
    };
  },
};
</script>

<style lang="scss">
.f-artists {
  position: relative;
  height: 12em;
  width: calc(100% - 1em);
  background-color: #1f1e1d;
  padding: $small;
  border-radius: $small;
  user-select: none;
}

.f-artists .heading {
  color: #fff;
  margin: 0 0 1em 1em;
}

.f-artists .artists {
  position: absolute;
  bottom: 1em;
  width: calc(100% - 1em);
  height: 11em;
  display: flex;
  align-items: flex-end;
  flex-wrap: nowrap;
  overflow-y: scroll;
}

.f-artists .artists::-webkit-scrollbar {
  display: none;
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
}

.f-artists .artist:hover {
  transform: translateY(-1em);
  transition: all 0.5s ease-in-out;
}

.f-artists .artist-image {
  width: 7em;
  height: 7em;
  border-radius: 50%;
  margin-bottom: $small;
  background: url(../../assets/images/girl1.jpg);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.f-artists .c1 {
  position: relative;
  background: rgb(145, 42, 56);
  width: 15em;
  background-image: url(../../assets/images/gradient1.gif);
  overflow: hidden;
  margin-left: -0.1rem;
}

.f-artists .c1:hover > .s2 {
  background: rgba(53, 53, 146, 0.8);
  transition: all 0.5s ease;
  width: 12em;
  height: 12em;
}

.f-artists .c1 p {
  position: absolute;
  bottom: -2rem;
  margin-left: 0.5rem;
  z-index: 1;
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
}

.f-artists .artist-name {
  margin: 0;
  text-align: center;
  font-size: small;
}

.f-artists .blur {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0);
  backdrop-filter: blur(100px);
  -webkit-backdrop-filter: blur(100px);
  -moz-backdrop-filter: blur(100px);
  border-radius: $small;
}

.f-artists .s2 {
  position: absolute;
  left: -2em;
  bottom: -4em;
  width: 10em;
  height: 10em;
  background: rgba(53, 53, 146, 0.445);
  border-radius: 50%;
  transition: all 0.5s ease;
}
</style>