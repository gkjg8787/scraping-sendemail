from datetime import datetime

from domain.model import NoticeType, NoticeLog, INoticeLogFactory


class NoticeLogFactory(INoticeLogFactory):
    @classmethod
    def create(
        cls,
        log_id: int,
        notice_type: NoticeType,
        text: str,
        err_num: int,
        created_at: datetime,
    ) -> NoticeLog:
        if not notice_type:
            ValueError("notice_type is Empty")
        if not text:
            text = ""
        if not err_num:
            err_num = 0
        return NoticeLog(
            log_id=log_id,
            notice_type=notice_type,
            text=text,
            created_at=created_at,
            err_num=err_num,
        )
