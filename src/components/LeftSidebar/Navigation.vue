<template>
  <div id="nav-container">
    <router-link :to="{ name: 'Home' }">
      <div id="home-button">
        <div id="home-icon"></div>
        <span id="text">Home</span>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {};
</script>

<style>
#nav-container {
  color: #fff;
}

#nav-container #home-button {
  display: flex;
  align-items: center;
  justify-content: start;
}
#nav-container #home-button #home-icon {
  height: 30px;
  width: 30px;
  background-image: url(../../assets/icons/home.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  margin-right: 0.5em;
}

#nav-container #home-button #text {
  margin-top: 5px;
}
</style>