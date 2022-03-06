import { ref } from "@vue/reactivity";
import { reactive } from "vue";

const search_query = ref("");

const queue = ref([
  {
    title: "Nothing played yet",
    artists: ["... blah blah blah"],
    image: "http://0.0.0.0:8900/images/defaults/5.webp",
    _id: {
      $oid: "",
    },
  },
]);

const folder_song_list = ref([]);
const folder_list = ref([]);

const current = ref({
  title: "Nothing played yet",
  artists: ["... blah blah blah"],
  image: "http://0.0.0.0:8900/images/defaults/1.webp",
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

const album = reactive({
  tracklist: [],
  info: {},
  artists: [],
  bio: "",
});

const filters = ref([]);

const magic_flag = ref(false);
const loading = ref(false);

const is_playing = ref(false);

const settings = reactive({
  uri: "http://0.0.0.0:9876",
});

const tablist = {
  home: "home",
  search: "search",
  queue: "queue",
};

const current_tab = ref(tablist.home);

export default {
  search_query,
  queue,
  folder_song_list,
  folder_list,
  current,
  prev,
  filters,
  magic_flag,
  loading,
  is_playing,
  album,
  settings,
  current_tab,
  tablist
};
