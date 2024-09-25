from datetime import datetime, tzinfo, timezone

from domain.model import NoticeLog, INoticeLogRepository
from router.html.param import NoitceLogGetForm
from .shared import htmlcontext, htmlname, htmlelement, util as sutil


class NoticeLogResult(htmlcontext.HtmlContext):
    noticelog: NoticeLog
    error_msg: str = ""


class NoticeLogResultFactory:
    @classmethod
    def create(
        cls,
        noticelog: NoticeLog,
        err_msg: str = "",
        local_timezone: tzinfo | None = None,
    ) -> NoticeLogResult:
        cls.toLocaltimezone(noticelog, tz=local_timezone)
        return NoticeLogResult(noticelog=noticelog, err_msg=err_msg)

    @classmethod
    def toLocaltimezone(cls, log: NoticeLog, tz: tzinfo) -> None:
        log.created_at = sutil.utcTolocaltime(input_date=log.created_at, tz=tz)


class NoticeLogHTML:
    repostitory: INoticeLogRepository
    local_timezone: tzinfo
    log_id: int

    def __init__(
        self, log_id: int, repository: INoticeLogRepository, local_timezone: tzinfo
    ):
        self.repostitory = repository
        self.local_timezone = local_timezone
        self.log_id = log_id

    async def execute(self) -> NoticeLogResult:
        ret = await self.repostitory.find_by_log_id(self.log_id)
        return NoticeLogResultFactory.create(
            noticelog=ret, local_timezone=self.local_timezone
        )
