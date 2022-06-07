<template>
  <div
    class="title"
    v-show="$route.name == 'Playlists'"
    v-motion
    :initial="{
      opacity: 0,
      x: -20,
    }"
    :visible="{
      opacity: 1,
      x: 0,
      transition: {
        delay: 100,
      },
    }"
  >
    Playlists
  </div>
</template>
