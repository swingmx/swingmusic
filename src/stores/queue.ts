import { defineStore } from "pinia";
import state from "../composables/state";
import { useNotifStore, NotifType } from "./notification";

import {
  Track,
  fromFolder,
  fromAlbum,
  fromPlaylist,
  fromSearch,
} from "../interfaces";
import notif from "../composables/mediaNotification";
import { FromOptions } from "../composables/enums";

function writeQueue(
  from: fromFolder | fromAlbum | fromPlaylist,
  tracks: Track[]
) {
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

const defaultTrack = <Track>{
  title: "Nothing played yet",
  albumhash: " ",
  artists: ["Alice"],
  trackid: "",
  image: "",
};

type From = fromFolder | fromAlbum | fromPlaylist | fromSearch;

export default defineStore("Queue", {
  state: () => ({
    progressElem: HTMLElement,
    audio: new Audio(),
    duration: {
      current: 0,
      full: 0,
    },
    current: 0,
    next: 0,
    prev: 0,
    currentid: "",
    playing: false,
    from: <From>{},
    tracks: <Track[]>[defaultTrack],
  }),
  actions: {
    play(index: number = 0) {
      const track = this.tracks[index];
      this.current = index;
      this.currentid = track.trackid;
      const uri = state.settings.uri + "/file/" + track.trackid;
      const elem = document.getElementById("progress");
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
        .catch((err) => {
          console.error(err);
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
        const a = (pos / 100) * this.audio.duration;
        this.audio.currentTime = a;
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
        this.tracks = parsed.tracks;
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
      if (index == this.tracks.length - 1) {
        this.next = 0;
        return;
      }

      this.next = index + 1;
    },
    updatePrev(index: number) {
      if (index === 0) {
        this.prev = this.tracks.length - 1;
        return;
      }

      this.prev = index - 1;
    },
    setCurrent(index: number) {
      const track = this.tracks[index];

      this.current = index;
      this.currentid = track.trackid;
      this.duration.full = track.length;
    },
    setNewQueue(tracklist: Track[]) {
      if (this.tracks !== tracklist) {
        this.tracks = [];
        this.tracks.push(...tracklist);
        writeQueue(this.from, this.tracks);
      }
    },
    playFromFolder(fpath: string, tracks: Track[]) {
      this.from = <fromFolder>{
        type: FromOptions.folder,
        path: fpath,
        name: fpath.split("/").splice(-1).join(""),
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
      this.tracks.push(track);
      writeQueue(this.from, this.tracks);
      this.updateNext(this.current);
    },
    playTrackNext(track: Track) {
      const Toast = useNotifStore();
      if (this.current == this.tracks.length - 1) {
        this.tracks.push(track);
      } else {
        const nextindex = this.current + 1;
        const next: Track = this.tracks[nextindex];

        if (next.trackid === track.trackid) {
          Toast.showNotification("Track is already queued", NotifType.Info);
          return;
        }
      }

      this.tracks.splice(this.current + 1, 0, track);
      this.updateNext(this.current);
      Toast.showNotification(
        `Added ${track.title} to queue`,
        NotifType.Success
      );
      writeQueue(this.from, this.tracks);
    },
    clearQueue() {
      this.tracks = [defaultTrack] as Track[];
      this.current = 0;
      this.currentid = "";
      this.next = 0;
      this.prev = 0;
      this.from = <From>{};
      console.log(this.current);
    },
  },
});
