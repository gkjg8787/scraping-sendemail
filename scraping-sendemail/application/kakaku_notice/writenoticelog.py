from datetime import datetime, timezone

from domain.model import (
    INoticeLogFactory,
    INoticeLogRepository,
    NoticeType,
)
from domain.service import INoticeLogIdentity


class NoticeLogger:
    factory: INoticeLogFactory
    repository: INoticeLogRepository
    ididentity: INoticeLogIdentity

    def __init__(
        self,
        factory: INoticeLogFactory,
        repository: INoticeLogRepository,
        noticeididentity: INoticeLogIdentity,
    ):
        self.factory = factory
        self.repository = repository
        self.ididentity = noticeididentity

    async def _save_log(self, notice_type: NoticeType, text: str, err_num: int):
        log_id = await self.ididentity.next_identity()
        new_log = self.factory.create(
            log_id=log_id,
            notice_type=notice_type,
            text=text,
            err_num=err_num,
            created_at=datetime.now(timezone.utc),
        )
        await self.repository.save(new_log)

    async def check(self, text: str = "", api_flag: bool = False, err_num: int = 0):
        if not api_flag:
            notice_type = NoticeType.CHECK
        else:
            notice_type = NoticeType.API_CHECK
        await self._save_log(notice_type=notice_type, text=text, err_num=err_num)

    async def update_notice(self, text: str, err_num: int = 0):
        await self._save_log(
            notice_type=NoticeType.UPDATE_NOTICE, text=text, err_num=err_num
        )
