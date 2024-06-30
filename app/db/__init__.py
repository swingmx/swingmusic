from typing import Any

from sqlalchemy import (
    create_engine,
    delete,
    insert,
    select,
)

from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
)

# ============================================================
# TODO: Make sure the database is created before we run this.
fullpath = "/home/cwilvx/temp/swingmusic/swing.db"
engine = create_engine(
    f"sqlite+pysqlite:///{fullpath}",
    echo=False,
    max_overflow=0,
    pool_size=5,
)

# connection = engine.connect()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class DbManager:
    def __init__(self, commit: bool = False):
        self.commit = commit
        self.engine = create_engine(f"sqlite+pysqlite:///{fullpath}", echo=True)
        self.conn = self.engine.connect()

    def __enter__(self):
        return self.conn.execution_options(preserve_rowcount=True)
        # return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            self.conn.commit()

        self.conn.close()


class Base(MappedAsDataclass, DeclarativeBase):
    @classmethod
    def execute(cls, stmt: Any, commit: bool = False):
        with DbManager(commit=commit) as conn:
            return conn.execute(stmt)

    @classmethod
    def insert_many(cls, items: list[dict[str, Any]]):
        """
        Inserts multiple items into the database.
        """
        with DbManager(commit=True) as conn:
            return conn.execute(insert(cls).values(items))

    @classmethod
    def insert_one(cls, item: dict[str, Any]):
        """
        Inserts a single item into the database.
        """
        return cls.insert_many([item])

    @classmethod
    def remove_all(cls):
        with DbManager(commit=True) as conn:
            conn.execute(delete(cls))

    @classmethod
    def all(cls):
        return cls.execute(select(cls))


def create_all():
    Base().metadata.create_all(engine)
