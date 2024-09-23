from datetime import datetime
from abc import ABCMeta, abstractmethod

from .items import KakakuItem


class IKakakuItemFactory(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
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
        pass
