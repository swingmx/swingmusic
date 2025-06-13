from pprint import pprint
from swingmusic.db.userdata import UserTable
from swingmusic.lib.recipes import HomepageRoutine
from swingmusic.lib.recipes.artistmixes import ArtistMixes
from swingmusic.models.mix import Mix
from swingmusic.plugins.mixes import MixesPlugin
from swingmusic.store.homepage import HomepageStore


class BecauseYouListened(HomepageRoutine):
    store_keys = ["because_you_listened_to_artist", "artists_you_might_like"]

    @property
    def is_valid(self):
        return MixesPlugin().enabled

    def run(self):
        users = UserTable.get_all()

        for user in users:
            entry: dict[str, Mix] = HomepageStore.entries.get(
                ArtistMixes.store_key
            ).items.get(user.id)  # type: ignore

            if not entry:
                continue

            because_you_listened_to_artist, artists_you_might_like = (
                MixesPlugin().get_because_items(list(entry.values()))
            )

            HomepageStore.entries[self.store_keys[0]].items[
                user.id
            ] = because_you_listened_to_artist
            HomepageStore.entries[self.store_keys[1]].items[
                user.id
            ] = artists_you_might_like
