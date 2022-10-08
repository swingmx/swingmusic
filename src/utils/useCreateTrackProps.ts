import { Track } from "@/interfaces";
import queue from "@/stores/queue";

export default function createTrackProps(track: Track) {
  return {
    track,
    index: track.index + 1,
    isCurrent: queue().currentid === track.trackid,
    isCurrentPlaying:
      queue().currentid === track.trackid && queue().playing,
  };
}
