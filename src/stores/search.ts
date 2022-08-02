import { ref, reactive } from "@vue/reactivity";
import { defineStore } from "pinia";
import { AlbumInfo, Artist, Playlist, Track } from "../interfaces";
import {
  searchTracks,
  searchAlbums,
  searchArtists,
  loadMoreTracks,
  loadMoreAlbums,
  loadMoreArtists,
} from "../composables/fetch/searchMusic";
import { watch } from "vue";
import useDebouncedRef from "../composables/useDebouncedRef";
import useTabStore from "./tabs";
/**
 *
 * Scrolls on clicking the loadmore button
 */
function scrollOnLoad() {
  const elem = document.getElementById("tab-content");

  elem.scroll({
    top: elem.scrollHeight,
    left: 0,
    behavior: "smooth",
  });
}

export default defineStore("search", () => {
  const query = useDebouncedRef(null, 600);
  const currentTab = ref("tracks");
  const loadCounter = reactive({
    tracks: 0,
    albums: 0,
    artists: 0,
    playlists: 0,
  });

  const tracks = reactive({
    query: "",
    value: <Track[]>[],
    more: false,
  });

  const albums = reactive({
    query: "",
    value: <AlbumInfo[]>[],
    more: false,
  });

  const artists = reactive({
    query: "",
    value: <Artist[]>[],
    more: false,
  });

  const playlists = reactive({
    query: "",
    value: <Playlist[]>[],
    more: false,
  });

  /**
   * Searches for tracks, albums and artists
   * @param newquery query to search for
   */
  function fetchTracks(newquery: string) {
    searchTracks(newquery).then((res) => {
      tracks.value = res.tracks;
      tracks.more = res.more;
      tracks.query = newquery;
    });
  }

  function fetchAlbums(query: string) {
    searchAlbums(query).then((res) => {
      albums.value = res.albums;
      albums.more = res.more;
      albums.query = query;
    });
  }

  function fetchArtists(query: string) {
    searchArtists(query).then((res) => {
      artists.value = res.artists;
      artists.more = res.more;
      artists.query = query;
    });
  }

  /**
   * Loads more search tracks results
   *
   * @param index The starting index of the tracks to load
   */
  function loadTracks(index: number) {
    loadMoreTracks(index)
      .then((res) => {
        tracks.value = [...tracks.value, ...res.tracks];
        tracks.more = res.more;
      })
      .then(() => scrollOnLoad());
  }

  /**
   * Loads more search albums results
   *
   * @param index The starting index of the albums to load
   */
  function loadAlbums(index: number) {
    loadMoreAlbums(index)
      .then((res) => {
        albums.value = [...albums.value, ...res.albums];
        albums.more = res.more;
      })
      .then(() => scrollOnLoad());
  }

  /**
   * Loads more search artists results
   *
   * @param index The starting index of the artists to load
   */
  function loadArtists(index: number) {
    loadMoreArtists(index)
      .then((res) => {
        artists.value = [...artists.value, ...res.artists];
        artists.more = res.more;
      })
      .then(() => scrollOnLoad());
  }

  type loadType = "tracks" | "albums" | "artists" | "playlists";

  function updateLoadCounter(type: loadType) {
    switch (type) {
      case "tracks":
        loadCounter.tracks += 6;
        break;
      case "albums":
        loadCounter.albums += 6;
        break;
      case "artists":
        loadCounter.artists += 6;
        break;
    }
  }

  watch(
    () => query.value,
    (newQuery) => {
      for (const key in loadCounter) {
        loadCounter[key] = 0;
      }

      const tabs = useTabStore();

      if (tabs.current !== "search") {
        tabs.switchToSearch();
      }

      switch (currentTab.value) {
        case "tracks":
          fetchTracks(newQuery);
          break;
        case "albums":
          fetchAlbums(newQuery);
          break;
        case "artists":
          fetchArtists(newQuery);
          break;
        default:
          fetchTracks(newQuery);
          break;
      }
    }
  );

  watch(
    () => currentTab.value,
    (newTab) => {
      const current_query: string = query.value;

      switch (newTab) {
        case "tracks":
          if (tracks.query == current_query) break;
          fetchTracks(current_query);
          break;

        case "albums":
          if (albums.query == current_query) break;
          fetchAlbums(current_query);
          break;

        case "artists":
          if (artists.query == current_query) break;
          fetchArtists(current_query);
          break;
        default:
          fetchTracks(current_query);
          break;
      }
    }
  );

  function changeTab(tab: string) {
    currentTab.value = tab;
  }

  setTimeout(() => {}, 3000);

  return {
    tracks,
    albums,
    artists,
    playlists,
    query,
    currentTab,
    loadCounter,
    updateLoadCounter,
    loadTracks,
    loadAlbums,
    loadArtists,
    changeTab,
  };
});
