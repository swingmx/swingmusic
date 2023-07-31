class Migration:
    """
    Base migration class.
    """

    name: str
    """
    Name of the migration.
    """

    @staticmethod
    def migrate():
        """
        Code to run when migrating
        """
        pass
