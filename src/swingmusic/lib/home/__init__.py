from swingmusic.db.userdata import MixTable


def find_mix(mixid: str, sourcehash: str):
    """
    Find a mix in the homepage store or the db.
    """
    # Premium is imported lazily to avoid a circular import during startup:
    # this module is loaded very early (via store.homepageentries →
    # lib.home.recover_items), well before premium.__init__ can finish.
    from swingmusic.store.homepage import HomepageStore
    from swingmusic.premium import MixesPlugin

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
        # Custom (track) mixes require the premium Mixes plugin.
        if MixesPlugin is None:
            return None

        mix = MixesPlugin.get_track_mix(mix)

        if not mix:
            return None

    return mix.to_dict()
