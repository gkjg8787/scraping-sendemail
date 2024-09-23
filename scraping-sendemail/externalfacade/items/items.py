from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def toDict(self):
        dic = {}
        for col in self.__table__.columns:
            dic[col.name] = getattr(self, col.name)
        return dic


class NewestItem(Base):
    __tablename__ = "newestitem"

    item_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(insert_default="")
    url_id: Mapped[int] = mapped_column(insert_default=-1)
    url: Mapped[str] = mapped_column(insert_default="")
    price: Mapped[int] = mapped_column(insert_default=-1)
    trendrate: Mapped[float] = mapped_column(insert_default=0)
    salename: Mapped[str] = mapped_column(insert_default="")
    storename: Mapped[str] = mapped_column(insert_default="")
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    record_low: Mapped[int] = mapped_column(insert_default=-1)
    active_url: Mapped[int] = mapped_column(insert_default=0)

    def __repr__(self) -> str:
        return (
            "newestitem("
            f"item_id={self.item_id!r}"
            f", name={self.name!r}"
            f", url_id={self.url_id!r}"
            f", url={self.url!r}"
            f", price={self.price!r}"
            f", trendrate={self.trendrate!r}"
            f", salename={self.salename!r}"
            f", storename={self.storename!r}"
            f", updated_at={self.updated_at!r}"
            f", record_low={self.record_low!r}"
            f", active_url={self.active_url!r}"
            ")"
        )
