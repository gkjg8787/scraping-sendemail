from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domain.service import INoticeLogIdentity
from .notice import DBNoticeLog


class NoticeLogIdentity(INoticeLogIdentity):
    session: AsyncSession
    INIT_ID = 1

    def __init__(self, session: AsyncSession):
        self.session = session

    async def next_identity(self) -> str:
        db = self.session
        stmt = select(func.max(DBNoticeLog.log_id))
        ret = await db.scalar(stmt)
        if ret and int(ret) >= self.INIT_ID:
            return str(int(ret) + 1)
        return str(self.INIT_ID)
