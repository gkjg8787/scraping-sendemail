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


class DBNoticeLog(Base):
    __tablename__ = "noticelog"

    log_id: Mapped[int] = mapped_column(primary_key=True)
    notice_type: Mapped[str] = mapped_column(insert_default="")
    text: Mapped[str] = mapped_column(insert_default="")
    err_num: Mapped[int] = mapped_column(insert_default=0)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )

    def __repr__(self) -> str:
        return (
            "DBNoticeLog("
            f"log_id={self.log_id!r}"
            f", notice_type={self.notice_type!r}"
            f", text={self.text!r}"
            f", err_num={self.err_num!r}"
            f", created_at={self.created_at!r}"
            ")"
        )
