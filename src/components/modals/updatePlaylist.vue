<template>
  <form
    @submit.prevent="update_playlist"
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
      ref="dropZoneRef"
    />
    <div id="upload" class="rounded-sm" @click="selectFiles">
      <div>Click to upload cover image</div>
      <div
        id="update-pl-img-preview"
        class="image"
        :style="{
          backgroundImage: `url(${
            paths.images.playlist + props.playlist.image
          })`,
        }"
      />
    </div>
    <button class="circular btn-active">
      {{ clicked ? "Updating" : "Update" }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
// import { useDropZone } from "@vueuse/core";

import { updatePlaylist } from "@/composables/fetch/playlists";
import { paths } from "@/config";
import { Playlist } from "@/interfaces";
import usePStore from "@/stores/pages/playlist";

const pStore = usePStore();

const props = defineProps<{
  playlist: Playlist;
}>();

// const dropZoneRef = ref<HTMLDivElement>();
// const { isOverDropZone } = useDropZone(dropZoneRef, handleDrop);

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

// function handleDrop(files: File[] | null) {
//   if (files) {
//     handleFile(files[0]);
//   }
// }

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

let clicked = ref(false);

function update_playlist(e: Event) {
  const form = e.target as HTMLFormElement;
  const formData = new FormData(form);

  const name = formData.get("name") as string;

  const nameChanged = name !== props.playlist.name;
  const imgChanged = image !== undefined;

  if (!nameChanged && !imgChanged) {
    emit("hideModal");
    return;
  }

  clicked.value = true;

  formData.append("image", image);

  if (name && name.toString().trim() !== "") {
    updatePlaylist(props.playlist.id, formData, pStore).then(() => {
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
    cursor: pointer;

    #update-pl-img-preview {
      width: 4.5rem;
      height: 4.5rem;
      border-radius: $small;
      object-fit: cover;
      background-color: $gray4;
    }
  }
}
</style>
