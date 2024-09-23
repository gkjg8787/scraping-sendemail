from datetime import datetime
from abc import ABCMeta, abstractmethod

from .notice import NoticeLog, NoticeType


class INoticeLogRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, noticelog: NoticeLog):
        pass

    @abstractmethod
    async def find_by_date(self, target_date: datetime) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def find_by_noticetype(self, notice_type: NoticeType) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def find_by_err_num(self, err_num: int) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def find_all(self) -> list[NoticeLog]:
        pass

    @abstractmethod
    async def delete_by_older_than_date(
        self, target_date: datetime, including: bool = False
    ) -> None:
        pass
