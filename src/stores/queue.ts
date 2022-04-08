import { defineStore } from "pinia";
import state from "../composables/state";
import { Track, fromFolder, fromAlbum, fromPlaylist } from "../interfaces";
import notif from "../composables/mediaNotification";
import { FromOptions } from "../composables/enums";

function addQToLocalStorage(
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

function addCurrentToLocalStorage(track: Track) {
  localStorage.setItem("current", JSON.stringify(track));
}

function readCurrentFromLocalStorage(): Track {
  const current = localStorage.getItem("current");
  if (current) {
    return JSON.parse(current);
  }
  return defaultTrack;
}

const defaultTrack = <Track>{
  title: "Nothing played yet",
  artists: ["Alice"],
  trackid: "",
  image: "",
};

export default defineStore("Queue", {
  state: () => ({
    progressElem: HTMLElement,
    audio: new Audio(),
    current: <Track>{},
    next: <Track>{},
    prev: <Track>{},
    playing: false,
    current_time: 0,
    from: <fromFolder>{} || <fromAlbum>{} || <fromPlaylist>{},
    tracks: <Track[]>[defaultTrack],
  }),
  actions: {
    play(track: Track) {
      const uri = state.settings.uri + "/file/" + track.trackid;
      const elem = document.getElementById("progress");
      this.updateCurrent(track);

      new Promise((resolve, reject) => {
        this.audio.src = uri;
        this.audio.oncanplaythrough = resolve;
        this.audio.onerror = reject;
      })
        .then(() => {
          this.audio.play().then(() => {
            this.playing = true;
            notif(track, this.playPause, this.playNext, this.playPrev);

            this.audio.ontimeupdate = () => {
              this.current_time =
                (this.audio.currentTime / this.audio.duration) * 100;
              elem.style.backgroundSize = `${this.current_time}% 100%`;
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
    readQueueFromLocalStorage() {
      const queue = localStorage.getItem("queue");

      if (queue) {
        const parsed = JSON.parse(queue);
        this.from = parsed.from;
        this.tracks = parsed.tracks;
      }

      this.updateCurrent(readCurrentFromLocalStorage());
    },
    updateCurrent(track: Track) {
      this.current = track;

      this.updateNext(this.current);
      this.updatePrev(this.current);

      addCurrentToLocalStorage(track);
    },
    updateNext(track: Track) {
      const index = this.tracks.findIndex(
        (t: Track) => t.trackid == track.trackid
      );

      if (index == this.tracks.length - 1) {
        this.next = this.tracks[0];
      } else if (index == 0) {
        this.next = this.tracks[1];
      } else {
        this.next = this.tracks[index + 1];
      }
    },
    updatePrev(track: Track) {
      const index = this.tracks.findIndex(
        (t: Track) => t.trackid === track.trackid
      );

      if (index === 0) {
        this.prev = this.tracks[this.tracks.length - 1];
      } else if (index === this.tracks.length - 1) {
        this.prev = this.tracks[index - 1];
      } else {
        this.prev = this.tracks[index - 1];
      }
    },
    setNewQueue(tracklist: Track[]) {
      if (this.tracks !== tracklist) {
        this.tracks = tracklist;
        addQToLocalStorage(this.from, this.tracks);
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
    playFromAlbum(aname: string, albumartist: string, tracks: Track[]) {
      this.from = <fromAlbum>{
        type: FromOptions.album,
        name: aname,
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
  },
});
