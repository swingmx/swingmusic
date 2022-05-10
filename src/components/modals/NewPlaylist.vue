<template>
  <form @submit="create" class="new-p-form">
    <label for="name">Playlist name</label>
    <br />
    <input
      type="text"
      class="rounded"
      name="name"
      id="modal-playlist-name-input"
    />
    <br />
    <input type="submit" class="rounded" value="Create" />
  </form>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { createNewPlaylist } from "../../composables/playlists";
import { Track } from "../../interfaces";
import { Notification, NotifType } from "../../stores/notification";

const props = defineProps<{
  track: Track;
}>();

onMounted(() => {
  document.getElementById("modal-playlist-name-input").focus();
});

const emit = defineEmits<{
  (e: "title", title: string): void;
  (e: "hideModal"): void;
}>();

emit("title", "New Playlist");

function create(e: Event) {
  e.preventDefault();
  const name = (e.target as HTMLFormElement).elements["name"].value;

  if (name.trim()) {
    createNewPlaylist(name, props.track).then((status: boolean) => {
      if (status) {
        emit("hideModal");
      }
    });
  } else {
    new Notification(
      "Playlist name can't be empty",
      NotifType.Error
    );
  }
}
</script>

<style lang="scss">
.new-p-form {
  grid-gap: 1rem;
  margin-top: 1rem;

  label {
    font-size: 0.9rem;
    color: $gray1;
  }

  input[type="text"] {
    margin: $small 0;
    border: 2px solid $gray3;
    background-color: transparent;
    color: #fff;
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    outline: none;
  }

  input[type="submit"] {
    margin: $small 0;
    background-color: $accent;
    color: #fff;
    width: 7rem;
    padding: 0.75rem;
    font-size: 1rem;
    border: none;
    outline: none;
    cursor: pointer;
  }
}
</style>
