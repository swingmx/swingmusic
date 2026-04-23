"""
Recipes are a way to create mixes.
"""

from typing import Any, List
from abc import ABC, abstractmethod


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

        # Premium exception classes are imported lazily: this module is
        # loaded transitively during `premium.__init__` (via crons → recipes),
        # so any module-level `from swingmusic.premium import ...` here
        # would capture stub classes that never match the real exceptions
        # raised by compiled premium code.
        from swingmusic.premium import CloudError, LicenseError

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
