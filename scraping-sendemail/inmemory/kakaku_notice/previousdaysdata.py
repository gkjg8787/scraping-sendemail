from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


from domain.model import KakakuItem
from application.kakaku_notice import IPreviousDaysKakakuData

JST = ZoneInfo("Asia/Tokyo")


class PreviousDaysDictKakakuData(IPreviousDaysKakakuData):
    data: dict[int, KakakuItem]

    def __init__(self, data: dict[int, KakakuItem]):
        self.data = data

    async def get(self) -> list[KakakuItem]:
        result: list[KakakuItem] = []
        yesterday = datetime.now(JST) - timedelta(days=1)
        for d in self.data.values():
            if d.updated_at.date() == yesterday.date():
                result.append(d)
        return result
