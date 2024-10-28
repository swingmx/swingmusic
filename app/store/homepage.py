from app.models.mix import Mix
from app.store.tracks import TrackStore
from app.utils.auth import get_current_userid


class HomepageStore:
    entries = {
        "artist_mixes": {},
    }

    @classmethod
    def set_artist_mixes(cls, mixes: list[Mix], userid: int = 1):
        idmap = {mix.id[1:]: mix for mix in mixes}
        cls.entries["artist_mixes"][userid] = idmap

    @classmethod
    def get_artist_mixes(cls):
        return [
            {
                "type": "mix",
                "item": mix.to_dict(),
            }
            for mix in cls.entries["artist_mixes"]
            .get(get_current_userid(), {})
            .values()
        ]

    @classmethod
    def get_mix(cls, mixtype: str, mixid: str):
        return cls.entries[mixtype].get(get_current_userid(), {}).get(mixid).to_full_dict()
