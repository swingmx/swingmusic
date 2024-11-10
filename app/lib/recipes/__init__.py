"""
Recipes are a way to create mixes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.db.userdata import UserTable
from app.models.mix import Mix
from app.plugins.mixes import MixesPlugin
from app.store.homepage import HomepageStore


class HomepageRoutine(ABC):
    """
    A routine creates a row of homepage items.
    """

    title: str
    description: str

    items: List[Mix]
    extra: Dict[str, Any]

    @property
    @abstractmethod
    def is_valid(self) -> bool: ...

    def __init__(self) -> None:
        if not self.is_valid:
            return

        self.items = self.run()

    @abstractmethod
    def run(self) -> List[Mix]:
        """
        Creates the homepage items and saves them to the
        homepage store if self.is_valid is true.
        """
        ...


class ArtistMixes(HomepageRoutine):
    items: List[Mix] = []
    extra: Dict[str, Any] = {}
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

            HomepageStore.set_mixes(mixes, mixkey=self.store_key, userid=user.id)

    def __init__(self) -> None:
        super().__init__()
