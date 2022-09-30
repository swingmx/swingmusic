import { Setting, SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";
import { appWidthStrings } from "./../strings";

const settings = useSettingsStore;

const extend_to_full_width: Setting = {
  title: appWidthStrings.settings.extend,
  type: SettingType.binary,
  source: () => settings().extend_width,
  action: () => settings().toggleExtendWidth(),
  inactive: () => !settings().can_extend_width,
};

export default [extend_to_full_width];
