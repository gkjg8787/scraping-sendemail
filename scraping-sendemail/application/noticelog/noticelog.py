from datetime import datetime, timezone, timedelta

from domain.model import INoticeLogFactory, INoticeLogRepository, NoticeType, NoticeLog
from domain.service import INoticeLogIdentity
from settings import NOTICELOG
from application.localtime import get_localtimezone
from .noticelogconfig import NoticeLogConfig


class NoticeLogger:
    factory: INoticeLogFactory
    repository: INoticeLogRepository
    ididentity: INoticeLogIdentity

    def __init__(
        self,
        factory: INoticeLogFactory,
        repository: INoticeLogRepository,
        noticelogidentity: INoticeLogIdentity,
    ):
        self.factory = factory
        self.repository = repository
        self.ididentity = noticelogidentity

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


class NoticeLogOrganizer:
    repository: INoticeLogRepository
    noticelogconfig: NoticeLogConfig

    def __init__(
        self, repository: INoticeLogRepository, noticelogconfig: NoticeLogConfig
    ):
        self.repository = repository
        self.noticelogconfig = noticelogconfig

    async def execute(self):
        noticelogconfig: NoticeLogConfig = self.noticelogconfig
        if noticelogconfig.storagedays > 0:
            now = datetime.now(get_localtimezone())
            target_date = now - timedelta(days=noticelogconfig.storagedays)
            await self.repository.delete_by_older_than_date(target_date=target_date)

        if noticelogconfig.storagecount > 0:
            ret = await self.repository.find_all()
            if len(ret) > noticelogconfig.storagecount:
                delete_list: list[NoticeLog] = []
                get_count = len(ret) - noticelogconfig.storagecount
                for log in sorted(ret, key=lambda l: l.log_id):
                    delete_list.append(log)
                    if get_count <= len(delete_list):
                        break
                for log in delete_list:
                    await self.repository.delete_by_log_id(log.log_id)
