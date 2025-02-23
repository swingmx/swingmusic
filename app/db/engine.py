from contextlib import contextmanager
from sqlalchemy import Engine, event
from sqlalchemy.orm import sessionmaker


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=10000")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA temp_store=FILE")
    cursor.execute("PRAGMA mmap_size=0")
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
        Session = sessionmaker(cls.engine)

        try:
            with Session() as session:
                yield session

                if commit:
                    session.commit()
                # yield session.execution_options(preserve_rowcount=True, yield_per=100)
            # yield conn.execution_options(preserve_rowcount=True, yield_per=100)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            if commit:
                session.commit()

            session.close()
            # del conn
            # cls.engine.clear_compiled_cache()
