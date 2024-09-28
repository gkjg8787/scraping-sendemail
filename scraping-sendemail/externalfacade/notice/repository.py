from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete


from domain.model import INoticeLogRepository, NoticeLog, NoticeType
from .dbconvert import DBToDomain, DomainToDB
from .notice import DBNoticeLog
from .factory import NoticeLogFactory


class NoticeLogRepository(INoticeLogRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, noticelog: NoticeLog):
        db = self.session
        db_log: DBNoticeLog | None = await db.get(DBNoticeLog, noticelog.log_id)
        new_log = DomainToDB.toDBNoticeLog(noticelog)
        if not db_log:
            db.add(new_log)
            await db.commit()
            await db.refresh(new_log)
            return
        elif db_log != new_log:
            db_log.notice_type = new_log.notice_type
            db_log.text = new_log.text
            db_log.err_num = new_log.err_num
            db_log.created_at = new_log.created_at
            await db.commit()
            await db.refresh(db_log)
            return

    async def find_by_log_id(self, log_id: int) -> NoticeLog | None:
        db = self.session
        db_log = await db.get(DBNoticeLog, log_id)
        if not db_log:
            return None
        result = DBToDomain(noticelogfactory=NoticeLogFactory()).toNoticeLog(db_log)
        return result

    @classmethod
    def _to_noticelog(cls, select_results):
        dbtodomain = DBToDomain(noticelogfactory=NoticeLogFactory())
        results = [dbtodomain.toNoticeLog(r) for r in select_results]
        return results

    async def find_by_filter(
        self,
        notice_type: NoticeType | None = None,
        err_num: int | None = None,
        target_date: datetime | None = None,
        keyword: str | None = None,
    ) -> list[NoticeLog]:
        db = self.session
        stmt = select(DBNoticeLog)
        if notice_type is not None:
            stmt = stmt.where(DBNoticeLog.notice_type == notice_type.value)
        if err_num is not None:
            stmt = stmt.where(DBNoticeLog.err_num == err_num)
        if target_date:
            target = target_date.replace(tzinfo=None)
            stmt = stmt.where(func.date(DBNoticeLog.created_at) == func.date(target))
        if keyword:
            stmt = stmt.where(DBNoticeLog.text.contains(keyword))
        stmt = stmt.order_by(DBNoticeLog.log_id.asc())
        ret = await db.scalars(stmt)
        return self._to_noticelog(ret.all())

    async def find_all(self) -> list[NoticeLog]:
        db = self.session
        stmt = select(DBNoticeLog).order_by(DBNoticeLog.log_id.asc())
        ret = await db.scalars(stmt)
        return self._to_noticelog(ret.all())

    async def delete_by_older_than_date(
        self, target_date: datetime, including: bool = False
    ) -> None:
        db = self.session
        target = target_date.replace(tzinfo=None)
        if not including:
            stmt = delete(DBNoticeLog).where(
                func.date(DBNoticeLog.created_at) < func.date(target)
            )
        else:
            stmt = delete(DBNoticeLog).where(
                func.date(DBNoticeLog.created_at) <= func.date(target)
            )
        await db.execute(stmt)
        await db.commit()

    async def delete_by_log_id(self, log_id: int):
        db = self.session
        stmt = delete(DBNoticeLog).where(DBNoticeLog.log_id == log_id)
        await db.execute(stmt)
        await db.commit()
