from datetime import datetime
from zoneinfo import ZoneInfo

from domain.model import KakakuItem
from externalfacade.items import KakakuItemFactory


JST = ZoneInfo("Asia/Tokyo")


def create_kakakuitem(
    item_id: int = 1,
    name: str = "",
    url_id: int = 1,
    url: str = "",
    price: int | None = None,
    trendrate: float | None = None,
    salename: str = "",
    storename: str = "",
    updated_at: datetime | None = None,
    record_low: int | None = None,
    active_url: int | None = None,
) -> KakakuItem:
    if not updated_at:
        updated_at = datetime.now(JST)
    return KakakuItemFactory.create(
        item_id=item_id,
        name=name,
        url_id=url_id,
        url=url,
        price=price,
        trendrate=trendrate,
        salename=salename,
        storename=storename,
        updated_at=updated_at,
        record_low=record_low,
        active_url=active_url,
    )
