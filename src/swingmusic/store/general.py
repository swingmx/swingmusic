from swingmusic.config import UserConfig
from swingmusic.models.user import User
from swingmusic.utils import classproperty


class GeneralStore:
    """
    This store can be used to track various states
    """

    admin_exists: bool = False
    root_dirs_set: bool = False
    scan_message: str = ""

    @classproperty
    def onboarding_complete(cls):
        return cls.admin_exists and cls.root_dirs_set

    @classmethod
    def load_onboarding_data(cls, users: list[User]):
        # INFO: Check if there are any users in the db
        if not users:
            cls.admin_exists = False

        for user in users:
            if "admin" in user.roles:
                cls.admin_exists = True
                break

        if UserConfig().rootDirs:
            cls.root_dirs_set = True
