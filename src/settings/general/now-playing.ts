import { Setting, SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

const use_alt_np: Setting = {
  title: "Use alternate now playing card",
  type: SettingType.switch,
  source: () => settings().use_alt_np,
  inactive: () => settings().disable_show_alt_np,
  action: () => settings().toggleUseRightNP(),
};
const use_sidebar: Setting = {
  title: "Use right sidebar",
  type: SettingType.switch,
  source: () => settings().use_sidebar,
  action: () => settings().toggleDisableSidebar(),
};

export default [use_sidebar, use_alt_np];
