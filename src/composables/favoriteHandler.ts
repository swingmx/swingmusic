import { favType } from "./enums";
import { addFavorite, removeFavorite } from "./fetch/favorite";
import useQueueStore from "@/stores/queue";
/**
 * Handles the favorite state of an item.
 * @param setter The ref to track the is_favorite state
 * @param type The type of item
 * @param itemhash The hash of the item
 */
export default async function favoriteHandler(
  flag: boolean | undefined,
  type: favType,
  itemhash: string,
  setter: (x?: unknown) => void,
  remover: (x?: unknown) => void
) {
  const queue = useQueueStore();
  const is_current =
    type === favType.track && itemhash === queue.currenttrackhash;
  if (flag) {
    const removed = await removeFavorite(type, itemhash);
    if (removed) remover();
  } else {
    const added = await addFavorite(type, itemhash);
    if (added) setter();
  }

  if (is_current) {
    queue.toggleFav(queue.currentindex);
  }
}
