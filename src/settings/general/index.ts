import { SettingCategory } from "@/interfaces/settings";
import nowPlaying from "./now-playing";

export default {
  title: "General",
  groups: [
    {
      settings: [...nowPlaying],
    },
  ],
} as SettingCategory;
