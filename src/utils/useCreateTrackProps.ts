import { Track } from "@/interfaces";
import queue from "@/stores/queue";
import { toRef } from "vue";

export default function createTrackProps(track: Track) {
  return {
    track,
    index: track.index + 1,
  };
}
