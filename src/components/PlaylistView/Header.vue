<template>
  <div class="p-header rounded">
    <div class="info rounded">
      <p class="name">Because I Got High Radio</p>
      <p class="text">
        The best music to fade to while doing my thing. Featuring artists like
        Wiz Khalifa, Lil Wayne, Ne-Yo, Ace Of Base, ...
      </p>
      <div class="lower">
        <div class="statistics">
          <div class="count s-item"><p>45 Tracks</p></div>
          <div class="duration s-item"><p>3 Hrs 45 Min</p></div>
        </div>
        <hr />
        <div class="btns">
          <div class="play s-item"><p>Play Now</p></div>
          <div class="options s-item image"></div>
        </div>
      </div>
      <!--  -->
      <div class="albums">
        <div class="item third image"></div>
        <div class="item second image"></div>
        <div class="item first image"></div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: 15rem;
  margin-bottom: 1em;
  background: rgb(42, 46, 54);
}

.p-header hr {
  border: none;
}

.p-header .info {
  background-color: rgb(1, 5, 17);
  padding: 0.5rem;
  position: relative;
  overflow: hidden;
}

.p-header .info .name {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 2rem;
  font-weight: bold;
  margin: 0.2em 0 0.5em 0;
}

.p-header .info .text {
  margin: 0.5rem 1em 0.5rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 4em;
}

.p-header .banner {
  margin: 0.5rem;
  background-color: $blue;
  background: url("../../assets/images/null.webp");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.p-header .info .statistics {
  display: flex;
}

.p-header .info .count {
  background: url(../../assets/icons/album.svg);
}

.p-header .info .duration {
  background-image: url(../../assets/icons/clock.svg);
}

.p-header .info .s-item {
  background-size: 1.2rem;
  background-position: 10% 50%;
  width: 9rem;
  display: flex;
  align-items: center;
  font-weight: lighter;
  margin-right: $small;
  height: 2rem;
  border: solid 1px rgba(255, 255, 255, 0.445);
  border-radius: $small;
  background-repeat: no-repeat;
}

.p-header .info .lower p {
  margin-left: 2.5rem;
}

.p-header .info .btns {
  height: 2.5rem;
  display: flex;
}

.p-header .info .btns .play {
  width: 8rem;
  height: 100%;
  background-color: $green;
  border: none;
  background-image: url(../../assets/icons/play.svg);
}

.p-header .info .btns .options {
  width: 2.5rem;
  height: 100%;
  background-color: #0465a7;
  border-radius: 50%;
  background-image: url(../../assets/icons/options.svg);
  background-size: 80%;
  background-position: center;
  border: none;
  transition: all 0.5s ease;
}

.p-header .info .btns .options:hover {
  transform: rotate(90deg);
  transition: all 0.5s ease;
  background-color: #2da8c7;
}

.p-header .info .albums {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 0.5rem;
  position: absolute;
  bottom: -0.5em;
  right: -1em;
}

.p-header .info .albums .item {
  height: 5em;
  width: 5em;
  background-color: $blue;
  border-radius: $small;
  transition: transform 1s;
}

.p-header .info .albums .first {
  position: absolute;
  transform: rotate(-30deg);
  right: 0.5em;
  bottom: 0em;
  background-color: $red;
  background-image: url("../../assets/images/null.webp");
}

.p-header .info .albums .second {
  position: absolute;
  transform: rotate(10deg);
  right: 4em;
  bottom: -1em !important;
  background-color: $green;
  background-image: url("../../assets/images/null.webp");
  z-index: 1;
}

.p-header .info .albums .third {
  position: absolute;
  transform: rotate(-10deg);
  bottom: -1em;
  right: 9em;
  background-color: $green;
  background-image: url("../../assets/images/null.webp");
  z-index: 2;
}

.p-header .info .albums .item:hover {
  transition: transform .5s;
  transform: scale(1.5);
  cursor: pointer;
  z-index: 3;
}
</style>
