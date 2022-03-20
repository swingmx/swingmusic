import { Track } from "../interfaces";
import Router from "../router";
import { Option } from "../interfaces";

/**
 * Returns a list of context menu items for a track.
 * @param  {any} track a track object.
 * @return {Array<Option>()} a list of context menu items.
 */

export default (track: Track): Array<Option> => {
  const single_artist = track.artists.length === 1;

  const children = () => {
    if (single_artist) {
      return false;
    }

    return track.artists.map((artist) => {
      return <Option>{
        label: artist,
        action: () => console.log("artist"),
      };
    });
  };

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
    label: single_artist ? "Go to Artist" : "Go to Artists",
    icon: "artist",
    action: () => {
      if (single_artist) {
        console.log("Go to Artist");
      }
    },
    children: children(),
  };

  const option7: Option = {
    label: "Go to Album Artist",
    action: () => console.log("Go to Album Artist"),
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

  const addToFav:Option = {
    label: "I love this",
    action: () => console.log("I love this"),
    icon: "heart",
  }

  const separator: Option = {
    type: "separator",
  };

  const options: Option[] = [
    option1,
    option2,
    addToFav,
    separator,
    option3,
    option4,
    option7,
    option5,
    separator,
    option6,
  ];

  return options;
};
