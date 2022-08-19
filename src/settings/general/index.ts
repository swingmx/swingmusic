import { SettingCategory } from "@/interfaces/settings";
import setNowPlayingComponent from "./now-playing";

console.log(setNowPlayingComponent);

export default {
  title: "General",
  groups: [
    {
      title: "Repeat queue",
      desc: "Do you want to do that?",
      settings: [setNowPlayingComponent()],
    },
  ],
} as SettingCategory;
