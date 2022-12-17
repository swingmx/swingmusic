import useAxios from "./useAxios";
import { paths } from "@/config";
import { favType, NotifType } from "@/composables/enums";

import { useNotifStore as notif } from "@/stores/notification";

export async function addFavorite(favtype: favType, itemhash: string) {
  const { data, error } = await useAxios({
    url: paths.api.favorite,
    props: {
      type: favtype,
      hash: itemhash,
    },
  });

  if (error) {
    notif().showNotification("Something funny happened!", NotifType.Error);
    return false;
  }

  if (data) {
    notif().showNotification("Added to favorites!", NotifType.Success);
  }

  return true;
}

export async function removeFavorite(favtype: favType, itemhash: string) {
  const { data, error } = await useAxios({
    url: paths.api.removeFavorite,
    props: {
      type: favtype,
      hash: itemhash,
    },
  });

  if (error) {
    notif().showNotification("Something funny happened!", NotifType.Error);
    return false;
  }

  if (data) {
    notif().showNotification("Removed from favorites!", NotifType.Error);
  }

  return true;
}
