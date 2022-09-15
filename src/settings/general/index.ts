import { SettingCategory } from "@/interfaces/settings";
import nowPlaying from "./now-playing";
import sidebarSettings from "./sidebar";
import extendWidth from "./extend-width";

export default {
  title: "General",
  groups: [
    {
      settings: [...sidebarSettings, ...nowPlaying, ...extendWidth],
    },
  ],
} as SettingCategory;
