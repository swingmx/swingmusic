import { defineStore } from "pinia";
import state from "../composables/state";
import { NotifType, useNotifStore } from "./notification";

import { FromOptions } from "../composables/enums";
import updateMediaNotif from "../composables/mediaNotification";

import {
  fromAlbum,
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

type From = fromFolder | fromAlbum | fromPlaylist | fromSearch;

let audio = new Audio();
let elem: HTMLElement;

export default defineStore("Queue", {
  state: () => ({
    duration: {
      current: 0,
      full: 0,
    },
    current: 0,
    next: 0,
    prev: 0,
    currentid: <string | null>"",
    playing: false,
    from: {} as From,
    currenttrack: {} as Track,
    tracklist: [] as Track[],
  }),
  actions: {
    bindProgressElem() {
      elem = document.getElementById("progress");
    },
    play(index: number = 0) {
      if (this.tracklist.length === 0) return;
      this.current = index;
      const track = this.tracklist[index];
      this.currentid = track.trackid;
      const uri = state.settings.uri + "/file/" + track.hash;
      this.updateCurrent(index);
      this.bindProgressElem();

      new Promise((resolve, reject) => {
        audio.autoplay = true;
        audio.src = uri;
        audio.oncanplaythrough = resolve;
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
              this.playNext();
            };
          });
        })
        .catch((err: ErrorEvent) => {
          err.stopImmediatePropagation();
          useNotifStore().showNotification(
            "Can't play: " + track.title,
            NotifType.Error
          );

          if (this.current !== this.tracklist.length - 1) {
            setTimeout(() => {
              this.playNext();
            }, 1000);
          }
        });
    },
    playPause() {
      if (audio.src === "") {
        this.play(this.current);
      } else if (audio.paused) {
        audio.play();
        this.playing = true;
      } else {
        audio.pause();
        this.playing = false;
      }
    },
    playNext() {
      this.play(this.next);
    },
    playPrev() {
      this.play(this.prev);
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
    updateCurrent(index: number) {
      this.setCurrent(index);
      this.updateNext(index);
      this.updatePrev(index);
    },
    updateNext(index: number) {
      if (index == this.tracklist.length - 1) {
        this.next = 0;
        return;
      }

      this.next = index + 1;
    },
    updatePrev(index: number) {
      if (index === 0) {
        this.prev = this.tracklist.length - 1;
        return;
      }

      this.prev = index - 1;
    },
    setCurrent(index: number) {
      const track = this.tracklist[index];

      this.currenttrack = track;
      this.current = index;
      this.currentid = track?.trackid || null;
      this.duration.full = track?.length || 0;
    },
    setNewQueue(tracklist: Track[]) {
      if (this.tracklist !== tracklist) {
        this.tracklist = [];
        this.tracklist.push(...tracklist);
      }
    },
    playFromFolder(fpath: string, tracks: Track[]) {
      this.from = <fromFolder>{
        type: FromOptions.folder,
        path: fpath,
        name: fpath?.split("/").splice(-1).join(""),
      };
      this.setNewQueue(tracks);
    },
    playFromAlbum(
      aname: string,
      albumartist: string,
      albumhash: string,
      tracks: Track[]
    ) {
      this.from = <fromAlbum>{
        type: FromOptions.album,
        name: aname,
        hash: albumhash,
        albumartist: albumartist,
      };

      this.setNewQueue(tracks);
    },
    playFromPlaylist(pname: string, pid: string, tracks: Track[]) {
      this.from = <fromPlaylist>{
        type: FromOptions.playlist,
        name: pname,
        playlistid: pid,
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
    addTrackToQueue(track: Track) {
      this.tracklist.push(track);
      // writeQueue(this.from, this.tracklist);
      this.updateNext(this.current);
    },
    playTrackNext(track: Track) {
      const Toast = useNotifStore();

      const nextindex = this.current + 1;
      const next: Track = this.tracklist[nextindex];

      // if track is already next, skip
      if (next?.trackid === track.trackid) {
        Toast.showNotification("Track is already queued", NotifType.Info);
        return;
      }

      // if tracklist is empty or current track is last, push track
      // else insert track after current track
      if (this.current == this.tracklist.length - 1) {
        this.tracklist.push(track);
      } else {
        this.tracklist.splice(this.current + 1, 0, track);
      }

      // save queue
      this.updateNext(this.current);
      Toast.showNotification(
        `Added ${track.title} to queue`,
        NotifType.Success
      );
    },
    clearQueue() {
      this.tracklist = [] as Track[];
      this.currentid = "";
      this.current, this.next, (this.prev = 0);
      this.from = <From>{};
    },
    shuffleQueue() {
      const Toast = useNotifStore();
      if (this.tracklist.length < 2) {
        Toast.showNotification("Queue is too short", NotifType.Info);
        return;
      }

      const shuffled = shuffle(this.tracklist);
      this.tracklist = shuffled;

      this.current = 0;
      this.play(this.current);

      this.currentid = shuffled[0].trackid;
      this.next = 1;
      this.prev = this.tracklist.length - 1;
    },
    removeFromQueue(index: number = 0) {
      this.tracklist.splice(index, 1);
    },
  },
  getters: {
    getNextTrack() {
      if (this.current == this.tracklist.length - 1) {
        return this.tracklist[0];
      } else {
        return this.tracklist[this.current + 1];
      }
    },
    getPrevTrack() {
      if (this.current === 0) {
        return this.tracklist[this.tracklist.length - 1];
      } else {
        return this.tracklist[this.current - 1];
      }
    },
    fullTime() {
      return audio.duration;
    },
    currentTime() {
      return audio.currentTime;
    },
    getCurrentTrack() {
      return this.tracklist[this.current];
    },
    getIsplaying() {
      return audio.paused ? false : true;
    },
  },
  persist: true,
});
