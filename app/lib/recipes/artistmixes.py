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

            custom_mixes = []
            for _mix in mixes:
                custom_mix = mix.get_custom_mix_items(_mix)

                if custom_mix:
                    custom_mixes.append(custom_mix)

            for index, custom_mix in enumerate(custom_mixes):
                custom_mix.title = f"Mix {index + 1}"

            HomepageStore.set_mixes(
                custom_mixes, entrykey="custom_mixes", userid=user.id
            )

    def __init__(self) -> None:
        super().__init__()
