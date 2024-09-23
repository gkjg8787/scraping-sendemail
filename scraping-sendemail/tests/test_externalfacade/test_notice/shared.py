from datetime import datetime
from zoneinfo import ZoneInfo

from domain.model import NoticeLog, NoticeType
from externalfacade.notice import NoticeLogFactory

JST = ZoneInfo("Asia/Tokyo")


def create_noticelog(
    log_id: int = 1,
    notice_type: NoticeType = NoticeType.CHECK,
    text: str = "",
    err_num: int = 0,
    created_at: datetime | None = None,
):
    if not created_at:
        created_at = datetime.now(JST)
    return NoticeLogFactory.create(
        log_id=log_id,
        notice_type=notice_type,
        text=text,
        err_num=err_num,
        created_at=created_at,
    )


def compare_noticelog(a: NoticeLog, b: NoticeLog) -> bool:
    if a.model_dump(exclude={"created_at"}) != b.model_dump(exclude={"created_at"}):
        return False
    return a.created_at.replace(tzinfo=None) == b.created_at.replace(tzinfo=None)
