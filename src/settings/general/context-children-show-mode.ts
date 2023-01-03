import { Setting } from "@/interfaces/settings";
import { SettingType } from "@/settings/enums";
import { contextChildrenShowModeStrings as showModeStr } from "./../strings";

import useSettingsStore from "@/stores/settings";
import { contextChildrenShowMode as mode } from "@/composables/enums";

const settings = useSettingsStore;

const context_children_show_mode: Setting = {
  title: showModeStr.settings.show_mode,
  type: SettingType.select,
  options: [
    {
      title: mode.click,
      value: mode.click,
    },
    {
      title: mode.hover,
      value: mode.hover,
    },
  ],
  source: () => settings().contextChildrenShowMode,
  action: (value: mode) => settings().setContextChildrenShowMode(value),
  defaultAction: () => settings().toggleContextChildrenShowMode(),
};

export default [context_children_show_mode];
