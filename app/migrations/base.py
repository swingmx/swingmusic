class Migration:
    """
    Base migration class.
    """
    enabled: bool = True

    @staticmethod
    def migrate():
        """
        Code to run when migrating, override this method.
        """
        pass
