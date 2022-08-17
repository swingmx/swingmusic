// @ts-strict

import { defineStore } from "pinia";
import state from "../composables/state";
import { NotifType, useNotifStore } from "./notification";

import { FromOptions } from "../composables/enums";
import notif from "../composables/mediaNotification";
import {
  fromAlbum,
  fromFolder,
  fromPlaylist,
  fromSearch,
  Track,
} from "../interfaces";

function writeQueue(from: From, tracks: Track[]) {
  localStorage.setItem(
    "queue",
    JSON.stringify({
      from: from,
      tracks: tracks,
    })
  );
}

function writeCurrent(index: number) {
  localStorage.setItem("current", JSON.stringify(index));
}

function readCurrent(): number {
  const current = localStorage.getItem("current");

  if (current) {
    return JSON.parse(current);
  }
  return 0;
}

function shuffle(tracks: Track[]) {
  const shuffled = tracks.slice();
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

type From = fromFolder | fromAlbum | fromPlaylist | fromSearch;

export default defineStore("Queue", {
  state: () => ({
    progressElem: HTMLElement,
    audio: new Audio(),
    duration: {
      current: 0,
      full: 0,
    },
    indexes: {
      current: 0,
      next: 0,
      previous: 0,
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
    play(index: number = 0) {
      if (this.tracklist.length === 0) return;
      this.current = index;
      const track = this.tracklist[index];
      this.currentid = track.trackid;
      const uri = state.settings.uri + "/file/" + track.hash;
      const elem = document.getElementById("progress") as HTMLElement;
      this.updateCurrent(index);

      new Promise((resolve, reject) => {
        this.audio.autoplay = true;
        this.audio.src = uri;
        this.audio.oncanplaythrough = resolve;
        this.audio.onerror = reject;
      })
        .then(() => {
          this.duration.full = this.audio.duration;
          this.audio.play().then(() => {
            this.playing = true;
            notif(track, this.playPause, this.playNext, this.playPrev);

            this.audio.ontimeupdate = () => {
              this.duration.current = this.audio.currentTime;
              const bg_size =
                (this.audio.currentTime / this.audio.duration) * 100;
              elem.style.backgroundSize = `${bg_size}% 100%`;
            };

            this.audio.onended = () => {
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
      if (this.audio.src === "") {
        this.play(this.current);
      } else if (this.audio.paused) {
        this.audio.play();
        this.playing = true;
      } else {
        this.audio.pause();
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
        this.audio.currentTime = pos;
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

      this.updateCurrent(readCurrent());
    },
    updateCurrent(index: number) {
      this.setCurrent(index);
      this.updateNext(index);
      this.updatePrev(index);

      writeCurrent(index);
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
        writeQueue(this.from, this.tracklist);
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
      writeQueue(this.from, this.tracklist);
      this.updateNext(this.current);
    },
    playTrackNext(track: Track) {
      const Toast = useNotifStore();
      if (this.current == this.tracklist.length - 1) {
        this.tracklist.push(track);
      } else {
        const nextindex = this.current + 1;
        const next: Track = this.tracklist[nextindex];

        if (next.trackid === track.trackid) {
          Toast.showNotification("Track is already queued", NotifType.Info);
          return;
        }
      }

      this.tracklist.splice(this.current + 1, 0, track);
      this.updateNext(this.current);
      Toast.showNotification(
        `Added ${track.title} to queue`,
        NotifType.Success
      );
      writeQueue(this.from, this.tracklist);
    },
    clearQueue() {
      this.tracklist = [] as Track[];
      this.currentid = "";
      this.current, this.next, (this.prev = 0);
      this.from = <From>{};

      writeCurrent(0);
      writeQueue(this.from, [] as Track[]);
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

      writeQueue(this.from, shuffled);
      writeCurrent(0);
    },
    removeFromQueue(index: number = 0) {
      this.tracklist.splice(index, 1);
    },
  },
});
