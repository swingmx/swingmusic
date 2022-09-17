import { Setting, SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

const use_alt_np: Setting = {
  title: "Use alternate now playing card",
  type: SettingType.binary,
  source: () => settings().use_alt_np,
  inactive: () => settings().disable_show_alt_np,
  action: () => settings().toggleUseRightNP(),
};

export default [use_alt_np];
