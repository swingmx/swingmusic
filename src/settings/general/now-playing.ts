import { SettingType } from "@/interfaces/settings";
import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore;

export default [
  {
    title: "Use left now playing card",
    type: SettingType.switch,
    source: () => settings().use_side_np,
    action: () => settings().toggleUseSideNP(),
  },
  {
    title: "Use right bottom now playing card",
    type: SettingType.switch,
    source: () => settings().use_right_np,
    action: () => settings().toggleUseRightNP(),
  },
];
