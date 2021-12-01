<template>
  <div class="up-next">
    <p class="heading">
      COMING UP NEXT <span class="more" @click="collapse">SEE ALL</span>
    </p>
    <div class="main-item h-1">
      <div class="album-art image"></div>
      <div class="tags">
        <p class="title">Hard to forget</p>
        <hr />
        <p class="artist">Sam hunt</p>
      </div>
    </div>
    <div class="all-items" v-if="!toggle">
      <div class="scrollable">
        <div class="song-item h-1" v-for="song in songs" :key="song">
          <div class="album-art image"></div>
          <div class="tags">
            <p class="title">{{ song.title }}</p>
            <hr />
            <p class="artist">{{ song.artist }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";

export default {
  props: ["up_next"],
  emits: ["updateCollapser"],
  setup(props, context) {
    const songs = [
      {
        title: "Hard to forget",
        artist: "Sam Hunt",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
      {
        title: "Bluebird",
        artist: "Miranda Lambert",
      },
      {
        title: "I called mama",
        artist: "Ken Chesseny",
      },
    ];

    const toggle = ref(props.up_next);

    let collapse = () => {
      context.emit("updateCollapser");
    };

    return { songs, collapse, toggle };
  },
};
</script>

<style>
.up-next {
  padding: 0.5rem;
  margin-top: 1rem;
  background-color: #131313b2;
  border-radius: 0.5rem;
}

.up-next .heading {
  position: relative;
  margin: 0.5rem 0 1rem 0rem;
}

.up-next > p > span {
  position: absolute;
  right: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  user-select: none;
}

.up-next > p > span:hover {
  background: rgb(62, 69, 77);
  cursor: pointer;
}

.up-next .main-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.up-next .main-item .album-art {
  width: 4.5rem;
  height: 4.5rem;
  background-color: #ccc;
  margin: 0 0.5rem 0 0;
  border-radius: 0.5rem;
  background-image: url(../../assets/images/htf.jpeg);
}

.up-next .main-item .tags hr {
  border: none;
  margin: 0.3rem;
}

.up-next .main-item .tags .title {
  width: 20rem;
  margin: 0;
}

.up-next .main-item .tags .artist {
  width: 20rem;
  margin: 0;
  font-size: small;
  color: rgba(255, 255, 255, 0.61);
}

.up-next .all-items {
  border-top: 1px solid var(--seperator);
}

.up-next .all-items .scrollable {
  height: 20rem;
  overflow-y: scroll;
  padding: 0.5rem;
  margin-top: 0.5rem;
  background-color: rgba(2, 6, 14, 0.425);
  border-radius: 0.5rem;
}

.up-next .all-items p {
  margin: 0;
}

.up-next .all-items .scrollable .song-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.up-next .all-items .scrollable .song-item:hover {
  cursor: pointer;
}

.up-next .all-items .scrollable .song-item hr {
  border: none;
  margin: 0.1rem;
}

.up-next .all-items .album-art {
  width: 3rem;
  height: 3rem;
  background-color: #ccc;
  margin: 0 0.5rem 0 0;
  border-radius: 0.5rem;
  background-image: url(../../assets/images/htf.jpeg);
}

.up-next .all-items .song-item .artist {
  font-size: small;
  color: rgba(255, 255, 255, 0.637);
}
</style>