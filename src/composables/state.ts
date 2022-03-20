import { ref } from "@vue/reactivity";
import { reactive } from "vue";
import * as i from "../interfaces";

const search_query = ref("");

const queue = ref(
  Array<i.Track>({
    title: "Nothing played yet",
    artists: ["... blah blah blah"],
    image: "http://127.0.0.1:8900/images/thumbnails/4.webp",
    trackid: "",
  })
);

const folder_song_list = ref([]);
const folder_list = ref([]);

const current = ref(<i.Track>{
  title: "Nothing played yet",
  artists: ["... blah blah blah"],
  image: "http://127.0.0.1:8900/images/thumbnails/4.webp",
  trackid: "",
});

const prev = ref(<i.Track>{
  title: "Nothing played yet",
  artists: ["... blah blah blah"],
  image: "http://127.0.0.1:8900/images/thumbnails/4.webp",
  trackid: "",
});

const album = reactive({
  tracklist: Array<i.Track>(),
  info: <i.AlbumInfo>{},
  artists: Array<i.Artist>(),
  bio: "",
});

const loading = ref(false);
const is_playing = ref(false);
const settings = reactive({
  uri: "http://127.0.0.1:9876",
});

export default {
  search_query,
  queue,
  folder_song_list,
  folder_list,
  current,
  prev,
  loading,
  is_playing,
  album,
  settings,
};
