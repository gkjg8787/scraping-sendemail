from datetime import datetime, timezone
from domain.model import NoticeLog, NoticeType
from externalfacade.notice import NoticeLogFactory


def create_noticelog(
    log_id: int = 1,
    notice_type: NoticeType = NoticeType.CHECK,
    text: str = "",
    err_num: int = 0,
    created_at: datetime | None = None,
) -> NoticeLog:
    if not created_at:
        created_at = datetime.now(timezone.utc)
    return NoticeLogFactory.create(
        log_id=log_id,
        notice_type=notice_type,
        text=text,
        err_num=err_num,
        created_at=created_at,
    )
