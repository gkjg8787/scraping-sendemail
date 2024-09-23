from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from domain.model import (
    KakakuItem,
    IKakakuItemRepository,
)
from .factory import KakakuItemFactory
from .dbconvert import DomainToDBObject, DBToDomain

from .items import NewestItem


class KakakuItemRepository(IKakakuItemRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, kakakuitem: KakakuItem):
        db = self.session
        db_item: NewestItem | None = await db.get(NewestItem, kakakuitem.item_id)
        new_item = DomainToDBObject.toNewestItem(kakakuitem)
        if not db_item:
            db.add(new_item)
            await db.commit()
            await db.refresh(new_item)
            return
        elif db_item != new_item:
            db_item.name = new_item.name
            db_item.url_id = new_item.url_id
            db_item.url = new_item.url
            db_item.price = new_item.price
            db_item.trendrate = new_item.trendrate
            db_item.salename = new_item.salename
            db_item.storename = new_item.storename
            db_item.updated_at = new_item.updated_at
            db_item.record_low = new_item.record_low
            db_item.active_url = new_item.active_url
            await db.commit()
            await db.refresh(db_item)
            return

    async def find_by_item_id(self, item_id: int) -> KakakuItem | None:
        db = self.session
        db_item: NewestItem | None = await db.get(NewestItem, item_id)
        if not db_item:
            return None
        dbtodomain = DBToDomain(kakakuitemfactory=KakakuItemFactory)
        return dbtodomain.toKakakuItem(newestitem=db_item)

    async def find_all(self) -> list[KakakuItem]:
        db = self.session
        stmt = select(NewestItem).order_by(NewestItem.item_id.asc())
        ret = await db.execute(stmt)
        results: list[KakakuItem] = []
        dbtodomain = DBToDomain(kakakuitemfactory=KakakuItemFactory)
        for r in ret.scalars().all():
            kakaku = dbtodomain.toKakakuItem(r)
            results.append(kakaku)
        return results

    async def delete_by_item_id(self, item_id: int) -> None:
        db = self.session
        db_item: NewestItem | None = await db.get(NewestItem, item_id)
        if not db_item:
            return
        await db.delete(db_item)
        await db.commit()
