import { ref, reactive } from "@vue/reactivity";
import { defineStore } from "pinia";
import { AlbumInfo, Artist, Track } from "../interfaces";
import {
  searchTracks,
  searchAlbums,
  searchArtists,
  loadMoreTracks,
  loadMoreAlbums,
  loadMoreArtists,
} from "../composables/searchMusic";
import { watch } from "vue";
import useDebouncedRef from "../composables/useDebouncedRef";

/**
 *
 * @param id  The id of the element of the div to scroll
 * Scrolls on clicking the loadmore button
 */
function scrollOnLoad(id: string) {
  const elem = document.getElementById(id);

  elem.scroll({
    top: elem.scrollHeight,
    left: 0,
    behavior: "smooth",
  });
}

export default defineStore("search", () => {
  const query = useDebouncedRef("", 600);

  const tracks = reactive({
    value: <Track[]>[],
    more: false,
  });

  const albums = reactive({
    value: <AlbumInfo[]>[],
    more: false,
  });

  const artists = reactive({
    value: <Artist[]>[],
    more: false,
  });

  /**
   * Searches for tracks, albums and artists
   * @param query query to search for
   */
  function search(query: string) {
    searchTracks(query).then((res) => {
      tracks.value = res.tracks;
      tracks.more = res.more;
    });

    searchAlbums(query).then((res) => {
      albums.value = res.albums;
      albums.more = res.more;
    });

    searchArtists(query).then((res) => {
      artists.value = res.artists;
      artists.more = res.more;
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
      .then(() => {
        scrollOnLoad("tab-content");
      });
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
      .then(() => {
        scrollOnLoad("tab-content");
      });
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
      .then(() => {
        scrollOnLoad("tab-content");
      });
  }

  watch(
    () => query.value,
    (newQuery) => {
      search(newQuery);
    }
  );

  return {
    tracks,
    albums,
    artists,
    query,
    search,
    loadTracks,
    loadAlbums,
    loadArtists,
  };
});
