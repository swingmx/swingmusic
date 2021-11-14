<template>
  <div class="container">
    <div class="l-sidebar"></div>
    <div class="nav">
      <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </div>
    </div>
    <div class="content">
      <router-view />
    </div>
    <div class="r-sidebar"></div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.container {
  display: grid;
  grid-template-columns: 50px 4fr 0fr;
  grid-template-rows: 0.1fr 1fr 1fr;
  /* grid-auto-columns: 1fr 1fr 1fr;
  grid-auto-rows: 1fr 1fr 1fr; */
  gap: 4px;
  grid-auto-flow: row;
  grid-template-areas:
    "l-sidebar nav nav"
    "l-sidebar content r-sidebar"
    "l-sidebar content r-sidebar";
  width: 100vw;
  height: 100vh;
}

.l-sidebar {
  grid-area: l-sidebar;
  border: solid;
  /* height: calc(100vh - 98px); */
}

.nav {
  grid-area: nav;
  border: solid;
  max-height: 70px;
}

.content {
  grid-area: content;
  border: solid;
}
body {
  margin: 0;
}

.r-sidebar {
  grid-area: r-sidebar;
  border: solid;
  /* max-width: 500px; */
}
</style>
