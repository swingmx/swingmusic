<template>
  <form
    @submit="update_playlist"
    class="new-p-form"
    enctype="multipart/form-data"
  >
    <label for="name">Playlist name</label>
    <br />
    <input
      type="text"
      class="rounded-sm"
      name="name"
      id="modal-playlist-name-input"
      :value="props.playlist.name"
    />
    <br />
    <input
      type="file"
      accept="image/*"
      name="image"
      id="update-pl-image-upload"
      style="display: none"
      @change="handleUpload"
    />
    <div id="upload" class="rounded-sm" @click="selectFiles">
      <div>Click to upload cover image</div>
      <div
        id="update-pl-img-preview"
        class="image"
        :style="{
          backgroundImage: `url(${props.playlist.image})`,
        }"
      />
    </div>
    <button type="submit" id="updateplaylistsubmit">Update</button>
  </form>
</template>

<script setup lang="ts">
import { updatePlaylist } from "@/composables/fetch/playlists";
import { Playlist } from "@/interfaces";
import usePStore from "@/stores/pages/playlist";
import { onMounted } from "vue";

const pStore = usePStore();

const props = defineProps<{
  playlist: Playlist;
}>();

onMounted(() => {
  (document.getElementById("modal-playlist-name-input") as HTMLElement).focus();
});

const emit = defineEmits<{
  (e: "setTitle", title: string): void;
  (e: "hideModal"): void;
}>();

emit("setTitle", "Update Playlist");

function selectFiles() {
  const input = document.getElementById(
    "update-pl-image-upload"
  ) as HTMLInputElement;
  input.click();
}

let image: File;

function handleUpload() {
  const input = document.getElementById(
    "update-pl-image-upload"
  ) as HTMLInputElement;

  if (input.files) {
    handleFile(input.files[0]);
  }
}

function handleFile(file: File) {
  if (!file || !file.type.startsWith("image/")) {
    return;
  }

  const preview = document.getElementById("update-pl-img-preview");
  const obj_url = URL.createObjectURL(file);

  if (preview) {
    preview.style.backgroundImage = `url(${obj_url})`;
  }

  image = file;
}

let clicked = false;

function update_playlist(e: Event) {
  e.preventDefault();

  if (!clicked) {
    clicked = true;
    const elem = document.getElementById(
      "updateplaylistsubmit"
    ) as HTMLButtonElement;
    elem.innerText = "Updating";
  } else {
    return;
  }

  const form = e.target as HTMLFormElement;
  const formData = new FormData(form);

  formData.append("image", image);

  if (formData.get("name").toString().trim() !== "") {
    updatePlaylist(props.playlist.playlistid, formData, pStore).then(() => {
      emit("hideModal");
    });
  }
}
</script>

<style lang="scss">
.new-p-form {
  #upload {
    width: 100%;
    padding: $small;
    border: solid 2px $gray3;
    display: grid;
    grid-template-columns: 1fr max-content;
    place-items: center;
    color: $gray1;
    margin: $small 0;

    #update-pl-img-preview {
      width: 4.5rem;
      height: 4.5rem;
      border-radius: $small;
      object-fit: cover;
      background-color: $gray4;
    }
  }

  textarea {
    width: 100%;
    max-width: 28rem;
    max-height: 5rem;
    color: $white;
    background-color: $gray2;
    border: none;
    font-family: inherit;
    padding: $small;
    outline: none;
    margin: $small 0;

    &:focus {
      outline: solid 2px $gray1;
    }
  }
}
</style>
