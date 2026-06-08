from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domain.model import KakakuItem
from application.kakaku_notice import IPreviousDaysKakakuData
from externalfacade.items import NewestItem, KakakuItemFactory
from externalfacade.items.dbconvert import DBToDomain


class GetAllKakakuData(IPreviousDaysKakakuData):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    def _to_kakakuitem(cls, select_results):
        dbtodomain = DBToDomain(kakakuitemfactory=KakakuItemFactory())
        results = [dbtodomain.toKakakuItem(r) for r in select_results]
        return results

    async def get(self) -> list[KakakuItem]:
        db = self.session
        stmt = select(NewestItem).order_by(NewestItem.item_id.asc())
        ret = await db.scalars(stmt)
        return self._to_kakakuitem(ret.all())
