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

    @classmethod
    def _to_noticelog(cls, select_results):
        dbtodomain = DBToDomain(noticelogfactory=NoticeLogFactory())
        results = [dbtodomain.toNoticeLog(r) for r in select_results]
        return results

    async def find_by_date(self, target_date: datetime) -> list[NoticeLog]:
        db = self.session
        target = target_date.replace(tzinfo=None)
        stmt = (
            select(DBNoticeLog)
            .where(func.date(DBNoticeLog.created_at) == func.date(target))
            .order_by(DBNoticeLog.log_id.asc())
        )
        ret = await db.scalars(stmt)
        return self._to_noticelog(ret.all())

    async def find_by_noticetype(self, notice_type: NoticeType) -> list[NoticeLog]:
        db = self.session
        stmt = (
            select(DBNoticeLog)
            .where(DBNoticeLog.notice_type == notice_type)
            .order_by(DBNoticeLog.log_id.asc())
        )
        ret = await db.scalars(stmt)
        return self._to_noticelog(ret.all())

    async def find_by_err_num(self, err_num: int) -> list[NoticeLog]:
        db = self.session
        stmt = (
            select(DBNoticeLog)
            .where(DBNoticeLog.err_num == err_num)
            .order_by(DBNoticeLog.log_id.asc())
        )
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
