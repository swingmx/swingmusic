from app.db.userdata import UserTable
from app.lib.recipes import HomepageRoutine
from app.plugins.mixes import MixesPlugin
from app.store.homepage import HomepageStore


class ArtistMixes(HomepageRoutine):
    store_key = "artist_mixes"

    @property
    def is_valid(self):
        return MixesPlugin().enabled

    def run(self):
        users = UserTable.get_all()

        for user in users:
            mix = MixesPlugin()
            mixes = mix.create_artist_mixes(user.id)

            if not mixes:
                continue

            HomepageStore.set_mixes(mixes, entrykey=self.store_key, userid=user.id)

    def __init__(self) -> None:
        super().__init__()