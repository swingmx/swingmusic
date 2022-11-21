import { Track } from "@/interfaces";
import queue from "@/stores/queue";

export default function createTrackProps(track: Track) {
  return {
    track,
    index: track.index + 1,
    isCurrent: queue().currentid === track.id,
    isCurrentPlaying:
      queue().currentid === track.id && queue().playing,
  };
}
