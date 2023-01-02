/**
 * Settings data strings
 */
interface S {
  title?: string;
  desc?: string;
  settings: {
    [key: string]: string;
  };
}

export const nowPlayingStrings = {
  title: "Now playing",
  desc: "Settings related to the current song",
  settings: {
    album_art: "Show album art on the left sidebar",
  },
} as S;

export const appWidthStrings = {
  settings: {
    extend: "Extend app to full screen width",
  },
} as S;

export const sidebarStrings = <S>{
  settings: {
    use_sidebar: "Show right sidebar",
  },
};

export const contextChildrenShowModeStrings = <S>{
  settings: {
    show_mode: "Show context children on",
  },
};

export const showFoldersAsStrings = <S>{
  settings: { show_folders_as: "Show folders as" },
};
