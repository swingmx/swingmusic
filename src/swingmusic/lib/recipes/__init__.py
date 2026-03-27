"""
Recipes are a way to create mixes.
"""

from typing import Any, List
from abc import ABC, abstractmethod

from swingmusic.lib.cloud import CloudError
from swingmusic.lib.license import LicenseError


class HomepageRoutine(ABC):
    """
    A routine creates a row of homepage items.
    """

    @property
    @abstractmethod
    def is_valid(self) -> bool: ...

    def __init__(self) -> None:
        if not self.is_valid:
            return

        try:
            self.run()
        except (LicenseError, CloudError) as e:
            print("Failed to run recipe")
            print(e)

    @abstractmethod
    def run(self) -> List[Any]:
        """
        Creates the homepage items and saves them to the
        homepage store if self.is_valid is true.
        """
        ...
