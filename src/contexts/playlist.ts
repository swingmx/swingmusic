import { Option } from "../interfaces";

export default async () => {
  const deletePlaylist: Option = {
    label: "Delete playlist",
    critical: true,
    action: () => {
      console.log("delete playlist");
    },
  };

  const playNext: Option = {
    label: "Play next",
    action: () => {
      console.log("play next");
    },
  };

  const addToQueue: Option = {
    label: "Add to queue",
    action: () => {
      console.log("add to queue");
    },
  };


  return [playNext, addToQueue, deletePlaylist];
};
