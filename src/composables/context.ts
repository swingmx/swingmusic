import { Ref } from "vue";

import useModalStore from "@/stores/modal";
import useQueueStore from "@/stores/queue";
import useContextStore from "@/stores/context";

import { ContextSrc } from "./enums";
import { Track } from "@/interfaces";
import trackContext from "@/contexts/track_context";

/**
 * Handles showing the context menu for a track component.
 * @param e The MouseEvent for positioning the context menu
 * @param track The track to link to the context menu
 * @param flag The boolean that manages the context visibility in the source component
 */
export const showTrackContextMenu = (
  e: MouseEvent,
  track: Track,
  flag: Ref<boolean>
) => {
  const menu = useContextStore();

  const options = () => trackContext(track, useModalStore, useQueueStore);

  menu.showContextMenu(e, options, ContextSrc.Track);
  flag.value = true;

  // watch for context menu visibility and reset flag
  menu.$subscribe((mutation, state) => {
    if (!state.visible) {
      flag.value = false;
    }
  });
};
