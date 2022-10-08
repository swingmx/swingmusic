import { SettingCategory } from "@/interfaces/settings";
import * as strings from "../strings";
import contextChildrenShowMode from "./context-children-show-mode";
import extendWidth from "./extend-width";
import nowPlaying from "./now-playing";
import sidebarSettings from "./sidebar";

const npStrings = strings.nowPlayingStrings;

export default {
  title: "General",
  groups: [
    {
      settings: [
        ...sidebarSettings,
        ...extendWidth,
        ...contextChildrenShowMode,
      ],
    },
    {
      title: npStrings.title,
      desc: npStrings.desc,
      settings: [...nowPlaying],
    },
  ],
} as SettingCategory;
