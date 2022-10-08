import { SettingType } from "../enums";
import { sidebarStrings } from "./../strings";
import { Setting } from "@/interfaces/settings";

import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

const use_sidebar: Setting = {
  title: sidebarStrings.settings.use_sidebar,
  type: SettingType.binary,
  source: () => settings().use_sidebar,
  action: () => settings().toggleDisableSidebar(),
};

export default [use_sidebar];
