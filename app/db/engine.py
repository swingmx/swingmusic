from contextlib import contextmanager
import gc
from sqlalchemy import Engine, event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=10000")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA temp_store=MEMORY")
    cursor.execute("PRAGMA mmap_size=30000000000")
    cursor.close()


class DbEngine:
    """
    The database engine instance.
    """

    engine: Engine

    @classmethod
    @contextmanager
    def manager(cls, commit: bool = False):
        """
        This context manager manages access to the database.

        When the context manager is entered, it returns a session object that can be used to execute SQL statements.

        If the `commit` parameter is set to `True`, the context manager will commit the transaction when it exits.
        """
        conn = cls.engine.connect()

        try:
            yield conn.execution_options(preserve_rowcount=True)
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
