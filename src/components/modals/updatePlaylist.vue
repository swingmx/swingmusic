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
      class="rounded"
      name="name"
      id="modal-playlist-name-input"
      :value="props.playlist.name"
    />
    <label for="name">Description</label>
    <br />
    <textarea
      name="description"
      id=""
      class="rounded"
      :value="props.playlist.description"
    ></textarea>
    <br />
    <input
      type="file"
      accept="image/*"
      name="image"
      id="update-pl-image-upload"
      style="display: none"
      @change="handleUpload"
    />
    <div
      id="upload"
      class="rounded"
      @click="selectFiles"
      @dragenter="dragEnter"
      @dragover="dragOver"
      @drop="drop"
    >
      <div>Click or Drag an image here</div>
      <div
        id="update-pl-img-preview"
        class="image"
        :style="{
          backgroundImage: `url(${props.playlist.image})`,
        }"
      />
    </div>
    <input type="submit" class="rounded" value="Update" />
  </form>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Playlist } from "../../interfaces";
import { updatePlaylist } from "../../composables/playlists";
import usePStore from "../../stores/p.ptracks";

const pStore = usePStore();

const props = defineProps<{
  playlist: Playlist;
}>();

onMounted(() => {
  document.getElementById("modal-playlist-name-input").focus();
});

const emit = defineEmits<{
  (e: "title", title: string): void;
  (e: "hideModal"): void;
}>();

emit("title", "Update Playlist");

let image: File;

function selectFiles() {
  const input = document.getElementById(
    "update-pl-image-upload"
  ) as HTMLInputElement;
  input.click();
}

function dragEnter(e: Event) {
  e.stopPropagation();
  e.preventDefault();
}

function dragOver(e: Event) {
  e.stopPropagation();
  e.preventDefault();
}

function drop(e: any) {
  e.stopImmediatePropagation();
  e.stopPropagation();
  e.preventDefault();

  const dt = e.dataTransfer;
  const files = dt.files;

  handleFile(files[0]);
}

function handleUpload() {
  const input = document.getElementById(
    "update-pl-image-upload"
  ) as HTMLInputElement;

  handleFile(input.files[0]);
}

function handleFile(file: File) {
  if (!file.type.startsWith("image/")) {
    return;
  }

  const preview = document.getElementById("update-pl-img-preview");
  const obj_url = URL.createObjectURL(file);
  preview.style.backgroundImage = `url(${obj_url})`;

  image = file;
}

function update_playlist(e: Event) {
  e.preventDefault();
  const form = e.target as HTMLFormElement;
  const formData = new FormData(form);
  formData.append("image", image);
  formData.append("lastUpdated", new Date().toString());

  console.log(formData.get("name") == "");

  if (formData.get("name").toString().trim() !== "") {
    updatePlaylist(props.playlist.playlistid, formData, pStore).then(() => {
      emit("hideModal");
    });
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

    &:focus {
      border: 2px solid transparent;
      outline: solid 2px $gray1;
    }
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

  #upload {
    width: 100%;
    padding: $small;
    border: solid 2px $gray3;
    display: grid;
    grid-template-columns: 1fr max-content;
    place-items: center;
    color: $gray1;
    margin: $small 0;
    cursor: pointer;

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
    background-color: transparent;
    border: solid 2px $gray3;
    font-family: inherit;
    padding: $small;
    outline: none;
    margin: $small 0;

    &:focus {
      border: 2px solid transparent;
      outline: solid 2px $gray1;
    }
  }

  .colors {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(2rem, 1fr));
    grid-gap: 0.5rem;
    margin: 0.5rem 0;

    .color {
      height: 2.5rem;
      width: 2.5rem;
      border-radius: 2rem;
    }

    .selected {
      border: 4px solid $white;
    }
  }
}
</style>
