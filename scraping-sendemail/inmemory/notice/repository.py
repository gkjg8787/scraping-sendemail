from datetime import datetime

from domain.model import INoticeLogRepository, NoticeLog, NoticeType


class NoticeLogDictRepository(INoticeLogRepository):
    data: dict[int, NoticeLog]

    def __init__(self, data: dict[int, NoticeLog]):
        self.data = data

    async def save(self, noticelog: NoticeLog):
        self.data[noticelog.log_id] = noticelog

    async def find_by_log_id(self, log_id: int) -> NoticeLog | None:
        return self.data.get(log_id, None)

    async def find_by_filter(
        self,
        notice_type: NoticeType | None = None,
        err_num: int | None = None,
        target_date: datetime | None = None,
        keyword: str | None = None,
    ) -> list[NoticeLog]:
        result: list[NoticeLog] = []
        for d in self.data.values():
            if (
                notice_type is None
                and err_num is None
                and target_date is None
                and keyword is None
            ):
                return list(self.data.values())
            hold = None
            if notice_type is not None:
                if d.notice_type == notice_type:
                    hold = d
            if err_num is not None:
                if not hold and d.err_num == err_num:
                    hold = d
                elif hold and hold.err_num != err_num:
                    hold = None
            if target_date is not None:
                if not hold and d.created_at.date() == target_date.date():
                    hold = d
                elif hold and hold.created_at.date() != target_date.date():
                    hold = None
            if keyword:
                if not hold and keyword in d.text:
                    hold = d
                elif hold and keyword not in hold.text:
                    hold = None
            if hold:
                result.append(hold)
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
