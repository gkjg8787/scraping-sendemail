from datetime import datetime
from abc import ABCMeta, abstractmethod

from .notice import NoticeLog, NoticeType


class INoticeLogRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, noticelog: NoticeLog):
        pass

    @abstractmethod
    async def find_by_log_id(self, log_id: int) -> NoticeLog | None:
        pass

    @abstractmethod
    async def find_by_filter(
        self,
        notice_type: NoticeType | None = None,
        err_num: int | None = None,
        target_date: datetime | None = None,
        keyword: str | None = None,
    ) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def find_all(self) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def delete_by_older_than_date(
        self, target_date: datetime, including: bool = False
    ) -> None:
        pass
