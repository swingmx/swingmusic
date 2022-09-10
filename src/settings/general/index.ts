import { SettingCategory } from "@/interfaces/settings";
import nowPlaying from "./now-playing";
import sidebarSettings from "./sidebar";

export default {
  title: "General",
  groups: [
    {
      settings: [...sidebarSettings, ...nowPlaying],
    },
  ],
} as SettingCategory;
