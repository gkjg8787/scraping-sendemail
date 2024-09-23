from domain.model import KakakuItem, IKakakuItemFactory
from .items import NewestItem


class DBToDomain:
    kakakuitemfactory: IKakakuItemFactory

    def __init__(self, kakakuitemfactory: IKakakuItemFactory):
        self.kakakuitemfactory = kakakuitemfactory

    def toKakakuItem(self, newestitem: NewestItem) -> KakakuItem:
        return self.kakakuitemfactory.create(
            item_id=newestitem.item_id,
            name=newestitem.name,
            url_id=newestitem.url_id,
            url=newestitem.url,
            price=newestitem.price,
            trendrate=newestitem.trendrate,
            salename=newestitem.salename,
            storename=newestitem.storename,
            updated_at=newestitem.updated_at,
            record_low=newestitem.record_low,
            active_url=newestitem.active_url,
        )


class DomainToDBObject:
    @classmethod
    def toNewestItem(cls, kakakuitem: KakakuItem) -> NewestItem:
        return NewestItem(
            item_id=kakakuitem.item_id,
            name=kakakuitem.name,
            url_id=kakakuitem.url_id,
            url=kakakuitem.url,
            price=kakakuitem.price,
            trendrate=kakakuitem.trendrate,
            salename=kakakuitem.salename,
            storename=kakakuitem.storename,
            updated_at=kakakuitem.updated_at,
            record_low=kakakuitem.record_low,
            active_url=kakakuitem.active_url,
        )
