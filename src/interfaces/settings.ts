import { SettingType } from "@/settings/enums";

export interface SettingOption {
  title: string;
  value: any;
}

export interface Setting {
  title: string;
  type: SettingType;
  options?: SettingOption[];
  inactive?: () => boolean;
  action: (arg0?: any) => void;
  source: () => any;
  defaultAction?: () => void;
}

export interface SettingGroup {
  title?: string;
  desc?: string;
  settings: Setting[];
}

export interface SettingCategory {
  title: string;
  groups: SettingGroup[];
}
