<template>
  <div class="now-playing">
    <div class="art-tags">
      <div class="album-art image"></div>
      <div>
        <p id="title" class="ellipsis">I love this bar (remix)</p>
        <hr />
        <span id="artist">Toby Keith, Morgan Wallen</span>
      </div>
    </div>
    <div class="controls">
      <div class="image" id="previous"></div>
      <div class="image" id="play-pause"></div>
      <div class="image" id="next"></div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.now-playing {
  height: 5rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #131313b2;

  display: grid;
  grid-template-columns: 3fr 1fr;
}

.now-playing .art-tags {
  display: flex;
  align-items: center;
}

.now-playing .art-tags .album-art {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 0.5rem;
  margin-right: 0.5rem;
  background-color: #ad1717a8;
  background-image: url(../../assets/images/tk.jpg);
}

.now-playing .art-tags hr {
  border: none;
  margin: 0.3rem;
}
.now-playing .art-tags #title {
  margin: 0;
  width: 14rem;
  color: #fff;
}

.now-playing .art-tags #artist {
  font-weight: lighter;
  font-size: small;
  color: rgba(255, 255, 255, 0.712);
}

.now-playing .controls {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: center;
}

.now-playing .controls * {
  height: 3rem;
  width: 3rem;
  background-size: 50%;
  cursor: pointer;
  border-radius: 0.5rem;
}

.now-playing .controls *:hover {
  filter: invert(66%) sepia(75%) saturate(4335%) hue-rotate(158deg)
    brightness(89%) contrast(101%);
}

.now-playing .controls #previous {
  background-image: url(../../assets/icons/previous.svg);
}

.now-playing .controls #play-pause {
  background-image: url(../../assets/icons/pause.svg);
}

.now-playing .controls #next {
  background-image: url(../../assets/icons/next.svg);
}
</style>