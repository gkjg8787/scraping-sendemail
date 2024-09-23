from datetime import datetime
from abc import ABCMeta, abstractmethod

from .notice import NoticeLog, NoticeType


class INoticeLogFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def create(
        cls,
        log_id: int,
        notice_type: NoticeType,
        text: str,
        err_num: int,
        created_at: datetime,
    ) -> NoticeLog:
        pass
