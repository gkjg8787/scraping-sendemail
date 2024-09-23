from datetime import datetime

from domain.model import (
    KakakuItem,
    IKakakuItemFactory,
)


class KakakuItemFactory(IKakakuItemFactory):
    @classmethod
    def create(
        cls,
        item_id: int,
        name: str,
        url_id: int,
        url: str,
        price: int,
        trendrate: float,
        salename: str,
        storename: str,
        updated_at: datetime,
        record_low: int,
        active_url: int,
    ) -> KakakuItem:
        if not name:
            name = ""
        if not url:
            url = ""
        if not price:
            price = -1
        if not trendrate:
            trendrate = 0.0
        if not salename:
            salename = ""
        if not record_low:
            record_low = -1
        if not active_url:
            active_url = 0
        return KakakuItem(
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
