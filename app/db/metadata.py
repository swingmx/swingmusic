from app.db import Base, DbManager


from sqlalchemy import Integer, insert, select, update
from sqlalchemy.orm import Mapped, mapped_column


class MigrationTable(Base):
    __tablename__ = "dbmigration"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[int] = mapped_column(Integer())

    @classmethod
    def set_version(cls, version: int):
        with DbManager(commit=True) as conn:
            result = conn.execute(
                update(cls).where(cls.id == 1).values(version=version)
            )

            if result.rowcount == 0:
                conn.execute(insert(cls).values(id=1, version=version))

    @classmethod
    def get_version(cls):
        with DbManager() as conn:
            result = conn.execute(select(cls.version).where(cls.id == 1))
            result = result.fetchone()

            if result:
                return result[0]

            return -1