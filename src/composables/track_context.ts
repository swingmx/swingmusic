import { Track } from './../interfaces';
import Router from "../router";

interface Option {
  type?: string;
  label?: string;
  action?: Function;
  icon?: string;
  critical?: Boolean;
}

/**
 * Returns a list of context menu items for a track.
 * @param  {any} track a track object.
 * @return {Array<Option>} a list of context menu items.
 */

export default (track: Track): Array<Option> => {
  const option1: Option = {
    label: "Add to Playlist",
    action: () => console.log("Add to Playlist"),
    icon: "plus",
  };

  const option2: Option = {
    label: "Add to Queue",
    action: () => console.log("Add to Queue"),
    icon: "add_to_queue",
  };

  const option3: Option = {
    label: "Go to Folder",
    action: () => {
      Router.push({
        name: "FolderView",
        params: { path: track.folder },
      });
    },
    icon: "folder",
  };

  const option4: Option = {
    label: "Go to Artist",
    action: () => console.log("Go to Artist"),
    icon: "artist",
  };

  const option5: Option = {
    label: "Go to Album",
    action: () => {
      Router.push({
        name: "AlbumView",
        params: { album: track.album, artist: track.albumartist },
      });
    },
    icon: "album",
  };

  const option6: Option = {
    label: "Delete Track",
    action: () => console.log("Delete Track"),
    icon: "delete",
    critical: true,
  };

  const separator: Option = {
    type: "separator",
  };

  const options: Option[] = [
    option1,
    option2,
    separator,
    option3,
    option4,
    option5,
    separator,
    option6,
  ];

  return options;
};
