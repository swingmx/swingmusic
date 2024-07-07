from contextlib import contextmanager
from sqlalchemy import Engine


class DbEngine:
    """
    The database engine instance.
    """

    engine: Engine

    @classmethod
    @contextmanager
    def manager(cls, commit: bool):
        """
        This context manager manages access to the database.

        When the context manager is entered, it returns a connection object that can be used to execute SQL statements.

        If the `commit` parameter is set to `True`, the context manager will commit the transaction when it exits.
        """

        try:
            conn = cls.engine.connect()
            yield conn.execution_options(preserve_rowcount=True)

            if commit:
                conn.commit()
        finally:
            conn.close()
