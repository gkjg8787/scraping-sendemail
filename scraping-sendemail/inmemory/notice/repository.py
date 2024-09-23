from datetime import datetime

from domain.model import INoticeLogRepository, NoticeLog, NoticeType


class NoticeLogDictRepository(INoticeLogRepository):
    data: dict[int, NoticeLog]

    def __init__(self, data: dict[int, NoticeLog]):
        self.data = data

    async def save(self, noticelog: NoticeLog):
        self.data[noticelog.log_id] = noticelog

    async def find_by_date(self, target_date: datetime) -> list[NoticeLog]:
        result: list[NoticeLog] = []
        for d in self.data.values():
            if d.created_at.date() == target_date.date():
                result.append(d)
        return result

    async def find_by_noticetype(self, notice_type: NoticeType) -> list[NoticeLog]:
        result: list[NoticeLog] = []
        for d in self.data.values():
            if d.notice_type == notice_type:
                result.append(d)
        return result

    async def find_by_err_num(self, err_num: int) -> list[NoticeLog]:
        result: list[NoticeLog] = []
        for d in self.data.values():
            if d.err_num == err_num:
                result.append(d)
        return result

    async def find_all(self) -> list[NoticeLog]:
        return list(self.data.values())

    async def delete_by_older_than_date(
        self, target_date: datetime, including: bool = False
    ) -> None:
        new_data: dict[int, NoticeLog] = {}
        target = target_date.replace(tzinfo=None)
        for d in self.data.values():
            if including and d.created_at.date() > target.date():
                new_data[d.log_id] = d
            elif not including and d.created_at.date() >= target.date():
                new_data[d.log_id] = d
        self.data = new_data
