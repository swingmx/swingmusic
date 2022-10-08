import { SettingType } from "../enums";
import { Setting } from "@/interfaces/settings";
import { nowPlayingStrings as data } from "../strings";

import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

const disable_np_img: Setting = {
  title: data.settings.album_art,
  type: SettingType.binary,
  source: () => settings().use_np_img,
  action: () => settings().toggleUseNPImg(),
};

export default [disable_np_img];
