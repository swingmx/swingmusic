from typing import Any

from sqlalchemy import (
    delete,
    func,
    insert,
    select,
)

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from app.db.engine import DbEngine


class Base(MappedAsDataclass, DeclarativeBase):
    """
    Base class for all database models.

    It has methods common to all tables. eg. `insert_one`, `insert_many`, `remove_all`, `remove_one`, `all`, `count`.
    """

    @classmethod
    def execute(cls, stmt: Any, commit: bool = False):
        with DbEngine.manager(commit=commit) as session:
            return session.execute(stmt)

    @classmethod
    def insert_many(cls, items: list[dict[str, Any]]):
        """
        Inserts multiple items into the database.
        """
        return cls.execute(insert(cls).values(items), commit=True)

    @classmethod
    def insert_one(cls, item: dict[str, Any]):
        """
        Inserts a single item into the database.
        """
        return cls.insert_many([item])

    @classmethod
    def remove_all(cls):
        return cls.execute(delete(cls), commit=True)

    @classmethod
    def remove_one(cls, id: int):
        return cls.execute(delete(cls).where(cls.id == id), commit=True)

    @classmethod
    def all(cls):
        return cls.execute(select(cls))

    @classmethod
    def count(cls):
        return cls.execute(select(func.count()).select_from(cls)).scalar()


def create_all_tables():
    """
    Creates all the tables that build on the Base class.
    """
    Base().metadata.create_all(DbEngine.engine)
