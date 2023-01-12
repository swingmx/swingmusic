import { paths } from "@/config";
import { defineStore } from "pinia";
import { Ref } from "vue";
import { NotifType, useNotifStore } from "./notification";

import { favType, FromOptions } from "../composables/enums";
import updateMediaNotif from "../composables/mediaNotification";
import { isFavorite } from "@/composables/fetch/favorite";
import useSettingsStore from "./settings";

import {
  fromAlbum,
  fromArtist,
  fromFav,
  fromFolder,
  fromPlaylist,
  fromSearch,
  Track,
} from "../interfaces";

function shuffle(tracks: Track[]) {
  const shuffled = tracks.slice();
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

type From =
  | fromFolder
  | fromAlbum
  | fromPlaylist
  | fromSearch
  | fromArtist
  | fromFav;

let audio = new Audio();
audio.autoplay = false;

export default defineStore("Queue", {
  state: () => ({
    duration: {
      current: 0,
      full: 0,
    },
    currentindex: 0,
    playing: false,
    from: {} as From,
    tracklist: [] as Track[],
    queueScrollFunction: (index: number) => {},
    mousover: <Ref | null>null,
  }),
  actions: {
    focusCurrentInSidebar(timeout = 500) {
      if (!this.mousover) {
        setTimeout(() => {
          this.queueScrollFunction(this.currentindex - 1);
        }, timeout);
      }
    },
    play(index: number = 0) {
      if (this.tracklist.length === 0) return;
      this.currentindex = index;
      this.focusCurrentInSidebar();

      const track = this.tracklist[index];
      const uri = `${paths.api.files}/${track.trackhash}`;

      new Promise((resolve, reject) => {
        audio.autoplay = true;
        audio.src = uri;
        audio.oncanplay = resolve;
        audio.onerror = reject;
      })
        .then(() => {
          this.duration.full = audio.duration;
          audio.play().then(() => {
            this.playing = true;
            updateMediaNotif();

            audio.ontimeupdate = () => {
              this.duration.current = audio.currentTime;
            };

            audio.onended = () => {
              this.autoPlayNext();
            };
          });
        })
        .catch((err: ErrorEvent) => {
          err.stopImmediatePropagation();
          useNotifStore().showNotification(
            "Can't play: " + track.title,
            NotifType.Error
          );
          if (this.currentindex !== this.tracklist.length - 1) {
            setTimeout(() => {
              if (!this.playing) return;
              this.autoPlayNext();
            }, 5000);
          }
        });
    },
    stop() {
      audio.src = "";
      this.playing = false;
    },
    playPause() {
      if (audio.src === "") {
        this.play(this.currentindex);
        return;
      }

      if (audio.paused) {
        audio.currentTime === 0 ? this.play(this.currentindex) : null;
        audio.play();
        this.playing = true;
      } else {
        audio.pause();
        this.playing = false;
      }
    },
    autoPlayNext() {
      const settings = useSettingsStore();
      const is_last = this.currentindex === this.tracklist.length - 1;

      if (settings.repeat_one) {
        this.play(this.currentindex);
        return;
      }

      if (settings.repeat_all) {
        this.play(is_last ? 0 : this.currentindex + 1);
        return;
      }

      const resetQueue = () => {
        this.currentindex = 0;
        this.playing = false;
        this.focusCurrentInSidebar();
      };

      !is_last ? this.play(this.currentindex + 1) : resetQueue();
    },
    playNext() {
      this.play(this.nextindex);
    },
    playPrev() {
      this.play(this.previndex);
    },
    seek(pos: number) {
      try {
        audio.currentTime = pos;
      } catch (error) {
        if (error instanceof TypeError) {
          console.error("Seek error: no audio");
        }
      }
    },
    readQueue() {
      const queue = localStorage.getItem("queue");

      if (queue) {
        const parsed = JSON.parse(queue);
        this.from = parsed.from;
        this.tracklist = parsed.tracks;
      }
    },
    setNewQueue(tracklist: Track[]) {
      if (this.tracklist !== tracklist) {
        this.tracklist = [];
        this.tracklist.push(...tracklist);
      }

      const settings = useSettingsStore();

      if (settings.repeat_one) {
        settings.toggleRepeatMode();
      }
      this.focusCurrentInSidebar(1000);
    },
    playFromFolder(fpath: string, tracks: Track[]) {
      console.log("play from folder");
      this.from = <fromFolder>{
        type: FromOptions.folder,
        path: fpath,
        name: "Folder: " + fpath.split("/").pop(),
      };
      this.setNewQueue(tracks);
    },
    playFromAlbum(aname: string, albumhash: string, tracks: Track[]) {
      this.from = <fromAlbum>{
        type: FromOptions.album,
        name: aname,
        albumhash: albumhash,
      };

      this.setNewQueue(tracks);
    },
    playFromPlaylist(pname: string, pid: string, tracks: Track[]) {
      this.from = <fromPlaylist>{
        type: FromOptions.playlist,
        name: pname,
        id: pid,
      };

      this.setNewQueue(tracks);
    },
    playFromSearch(query: string, tracks: Track[]) {
      this.from = <fromSearch>{
        type: FromOptions.search,
        query: query,
      };

      this.setNewQueue(tracks);
    },
    playFromArtist(artisthash: string, artistname: string, tracks: Track[]) {
      this.from = <fromArtist>{
        type: FromOptions.artist,
        artisthash: artisthash,
        artistname: artistname,
      };

      this.setNewQueue(tracks);
    },
    playFromFav(tracks: Track[]) {
      this.from = <fromFav>{
        type: FromOptions.favorite,
      };

      this.setNewQueue(tracks);
    },
    addTrackToQueue(track: Track) {
      this.tracklist.push(track);
    },
    playTrackNext(track: Track) {
      const Toast = useNotifStore();

      const nextindex = this.currentindex + 1;
      const next: Track = this.tracklist[nextindex];

      // if track is already next, skip
      if (next?.trackhash === track.trackhash) {
        Toast.showNotification("Track is already queued", NotifType.Info);
        return;
      }

      // if tracklist is empty or current track is last, push track
      // else insert track after current track
      if (this.currentindex == this.tracklist.length - 1) {
        this.tracklist.push(track);
      } else {
        this.tracklist.splice(this.currentindex + 1, 0, track);
      }

      // save queue
      Toast.showNotification(
        `Added ${track.title} to queue`,
        NotifType.Success
      );
    },
    clearQueue() {
      this.tracklist = [] as Track[];
      this.currentindex = 0;
      this.from = <From>{};
    },
    shuffleQueue() {
      const Toast = useNotifStore();
      if (this.tracklist.length < 2) {
        Toast.showNotification("Queue is too short", NotifType.Info);
        return;
      }

      const current = this.currenttrack;
      const current_hash = current?.trackhash;

      this.tracklist = shuffle(this.tracklist);
      // find current track after shuffle

      if (this.playing) {
        const newindex = this.tracklist.findIndex(
          (track) => track.trackhash === current_hash
        );

        // remove current track from queue
        this.tracklist.splice(newindex, 1);
        // insert current track at beginning of queue
        this.tracklist.unshift(current as Track);
        this.currentindex = 0;
        return;
      }

      this.currentindex = 0;
      this.play(this.currentindex);
    },
    removeFromQueue(index: number = 0) {
      if (index === this.currentindex) {
        const is_last = index === this.tracklist.length - 1;
        const was_playing = this.playing;

        audio.src = "";
        this.tracklist.splice(index, 1);

        if (is_last) {
          this.currentindex = 0;
        }

        if (was_playing) {
          this.playPause();
        }
      } else {
        this.tracklist.splice(index, 1);
      }
    },
    setScrollFunction(
      cb: (index: number) => void,
      mousover: Ref<boolean> | null
    ) {
      this.queueScrollFunction = cb;
      this.mousover = mousover;
    },
    toggleFav(index: number) {
      const track = this.tracklist[index];

      if (track) {
        track.is_favorite = !track.is_favorite;
      }
    },
  },
  getters: {
    next(): Track | undefined {
      if (this.currentindex == this.tracklist.length - 1) {
        return this.tracklist[0];
      } else {
        return this.tracklist[this.currentindex + 1];
      }
    },
    prev(): Track | undefined {
      if (this.currentindex === 0) {
        return this.tracklist[this.tracklist.length - 1];
      } else {
        return this.tracklist[this.currentindex - 1];
      }
    },
    currenttrack(): Track | undefined {
      const current = this.tracklist[this.currentindex];

      isFavorite(current?.trackhash || "", favType.track).then((is_fav) => {
        if (current) {
          current.is_favorite = is_fav;
        }
      });

      return current;
    },
    currenttrackhash(): string {
      return this.currenttrack?.trackhash || "";
    },
    previndex(): number {
      return this.currentindex === 0
        ? this.tracklist.length - 1
        : this.currentindex - 1;
    },
    nextindex(): number {
      return this.currentindex === this.tracklist.length - 1
        ? 0
        : this.currentindex + 1;
    },
  },
  persist: {
    afterRestore: (context) => {
      let store = context.store;
      store.duration.current = 0;
      store.playing = false;
    },
  },
});
