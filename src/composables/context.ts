import { Ref } from "vue";

import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";
import useContextStore from "@/stores/context";

import { ContextSrc } from "./enums";
import { Track } from "@/interfaces";
import trackContext from "@/contexts/track_context";

export const showTrackContextMenu = (
  e: MouseEvent,
  track: Track,
  flag: Ref<boolean>
) => {
  const menu = useContextStore();

  const options = () => trackContext(track, useModalStore, useQueueStore);

  menu.showContextMenu(e, options, ContextSrc.Track);
  flag.value = true;

  menu.$subscribe((mutation, state) => {
    if (!state.visible) {
      flag.value = false;
    }
  });
};
