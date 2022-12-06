import { Track } from "@/interfaces";
import queue from "@/stores/queue";

export default function createTrackProps(track: Track) {
  return {
    track,
    index: track.index + 1,
  };
}
