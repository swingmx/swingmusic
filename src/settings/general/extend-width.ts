import { Setting, SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

const extend_to_full_width: Setting = {
  title: "Extend app to full screen width",
  type: SettingType.binary,
  source: () => settings().extend_width,
  action: () => settings().toggleExtendWidth(),
  inactive: () => !settings().extend_width_enabled,
};

export default [extend_to_full_width];
