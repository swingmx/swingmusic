import { Ref } from "vue";
import { favType } from "./enums";
import { addFavorite, removeFavorite } from "./fetch/favorite";

/**
 * Handles the favorite state of an item.
 * @param flag The ref to track the is_favorite state
 * @param type The type of item
 * @param itemhash The hash of the item
 */
export default async function favoriteHandler(
  flag: Ref<boolean | undefined>,
  type: favType,
  itemhash: string
) {
  if (flag.value) {
    const removed = await removeFavorite(type, itemhash);

    if (removed) {
      flag.value = false;
    }

    return;
  }

  const added = await addFavorite(type, itemhash);

  if (added) {
    flag.value = true;
  }
}
