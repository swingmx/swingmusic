import { Track } from "@/interfaces";

export default function createTrackProps(track: Track) {
  return {
    track,
    index: track.index + 1,
  };
}
