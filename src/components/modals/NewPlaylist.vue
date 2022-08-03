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
    <div class="submit">
      <input type="submit" class="rounded" value="Create" />
    </div>
  </form>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { createNewPlaylist } from "../../composables/fetch/playlists";
import { Track } from "../../interfaces";
import { Notification, NotifType } from "../../stores/notification";
import usePlaylistStore from "@/stores/pages/playlists";

const props = defineProps<{
  track?: Track;
}>();
const route = useRoute();
const playlistStore = usePlaylistStore();

onMounted(() => {
  document.getElementById("modal-playlist-name-input").focus();
});

const emit = defineEmits<{
  (e: "title", title: string): void;
  (e: "hideModal"): void;
}>();

emit("title", "New Playlist");

/**
 * Create a new playlist. If this modal is called with a track,
 * add the track to the new playlist.
 * @param {Event} e
 */
function create(e: Event) {
  e.preventDefault();
  const name = (e.target as HTMLFormElement).elements["name"].value;

  if (name.trim()) {
    createNewPlaylist(name, props.track).then(({ success, playlist }) => {
      emit("hideModal");

      if (!success) return;

      if (route.name !== "Playlists") return;

      setTimeout(() => {
        playlistStore.addPlaylist(playlist);
      }, 600);
    });
  } else {
    new Notification("Playlist name can't be empty", NotifType.Error);
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

  .submit {
    display: flex;
    justify-content: flex-end;
  }

  input[type="submit"] {
    margin: $small 0;
    background-color: rgba(40, 132, 252, 0.884) !important;
    color: $white;
    padding: $small 1rem;
    font-size: 1rem;
    border: solid 2px transparent !important;
    outline: none;
    cursor: pointer;

    &:focus {
      border: 2px solid $gray1 !important;
    }
  }
}
</style>
