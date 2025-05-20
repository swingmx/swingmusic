from swingmusic.db.userdata import MixTable
from swingmusic.plugins.mixes import MixesPlugin


def find_mix(mixid: str, sourcehash: str):
    """
    Find a mix in the homepage store or the db.
    """
    from swingmusic.store.homepage import HomepageStore

    mixtype = "custom_mixes" if mixid[0] == "t" else "artist_mixes"

    # INFO: Try getting the mix from the homepage store
    mix = HomepageStore.get_mix(mixtype, mixid)
    if mix and mix["sourcehash"] == sourcehash:
        return mix

    # INFO: Get the mix from the db
    mix = MixTable.get_by_sourcehash(sourcehash)

    if not mix:
        return None

    if mixtype == "custom_mixes":
        mix = MixesPlugin.get_track_mix(mix)

        if not mix:
            return None

    return mix.to_dict()
