import { SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

export default [
  {
    title: "Use alternate now playing card",
    type: SettingType.switch,
    source: () => settings().use_alt_np,
    action: () => settings().toggleUseRightNP(),
  },
];
