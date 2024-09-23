from domain.service import INoticeLogIdentity
from domain.model import NoticeLog


class NoticeLogDictIdentity(INoticeLogIdentity):
    data: dict[int, NoticeLog]
    INIT_ID = 1

    def __init__(self, data: dict[int, NoticeLog]):
        self.data = data

    async def next_identity(self) -> str:
        if not self.data:
            return str(self.INIT_ID)
        return str(max(self.data.keys()) + 1)
