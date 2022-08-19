import { SettingType } from "@/interfaces/settings";

export default () => ({
  title: "Use Sidebar now playing card",
  type: SettingType.switch,
  action: () => console.log("should toggle something"),
});
