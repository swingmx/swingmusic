import { Setting, SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";
import { nowPlayingStrings as data } from "../strings";

const settings = useSettingsStore;

const disable_np_img: Setting = {
  title: data.settings.album_art,
  type: SettingType.binary,
  source: () => settings().use_np_img,
  action: () => settings().toggleUseNPImg(),
};

export default [disable_np_img];
