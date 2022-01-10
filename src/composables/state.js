import { ref } from "@vue/reactivity";

const search_query = ref("");

const queue = ref([
  {
    title: "Nothing played yet",
    artists: ["... blah blah blah"],
    _id: {
      $oid: "",
    },
  },
]);

const current = ref({
  title: "Nothing played yet",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const prev = ref({
  title: "The previous song",
  artists: ["... blah blah blah"],
  _id: {
    $oid: "",
  },
});

const filters = ref([]);
const magic_flag = ref(false);
const loading = ref(false);

const is_playing = ref(false);

const search_tracks = ref([]);
const search_albums = ref([]);
const search_artists = ref([]);

export default {
  search_query,
  queue,
  current,
  prev,
  filters,
  magic_flag,
  loading,
  is_playing,
  search_tracks,
  search_albums,
  search_artists,
};
