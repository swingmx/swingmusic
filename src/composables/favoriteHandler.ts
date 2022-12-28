import { favType } from "./enums";
import { addFavorite, removeFavorite } from "./fetch/favorite";

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
  setter: () => void,
  remover: () => void
) {
  if (flag) {
    const removed = await removeFavorite(type, itemhash);
    if (removed) remover();
    return;
  }

  const added = await addFavorite(type, itemhash);
  if (added) setter();
}
