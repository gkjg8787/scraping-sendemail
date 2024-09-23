import pytest

from domain.model import KakakuItem
from externalfacade.items import KakakuItemRepository, NewestItem, KakakuItemFactory
from externalfacade.items.dbconvert import DBToDomain

from tests.test_externalfacade.shared import create_kakakuitem, compare_kakakuitem


class TestKakakuItemRepository:
    @pytest.mark.asyncio
    async def test_save(self, test_db):
        async for db in test_db:
            repository = KakakuItemRepository(session=db)
            item = create_kakakuitem()
            await repository.save(item)
            db_ret: NewestItem = await db.get(NewestItem, item.item_id)
            dbto = DBToDomain(kakakuitemfactory=KakakuItemFactory())
            assert compare_kakakuitem(item, dbto.toKakakuItem(db_ret))

    @pytest.mark.asyncio
    async def test_find_by_item_id(self, test_db):
        async for db in test_db:
            repository = KakakuItemRepository(session=db)
            items = [
                create_kakakuitem(item_id=1, url_id=1),
                create_kakakuitem(item_id=2, url_id=2),
            ]
            for item in items:
                await repository.save(item)

            ret: KakakuItem = await repository.find_by_item_id(items[1].item_id)
            assert compare_kakakuitem(ret, items[1])

    @pytest.mark.asyncio
    async def test_find_all(self, test_db):
        async for db in test_db:
            repository = KakakuItemRepository(session=db)
            items = [
                create_kakakuitem(item_id=1, url_id=1),
                create_kakakuitem(item_id=2, url_id=2),
            ]
            for item in items:
                await repository.save(item)

            rets: KakakuItem = await repository.find_all()
            for a, b in zip(items, rets):
                assert compare_kakakuitem(a, b)

    @pytest.mark.asyncio
    async def test_delete_by_item_id(self, test_db):
        async for db in test_db:
            repository = KakakuItemRepository(session=db)
            items = [
                create_kakakuitem(item_id=1, url_id=1),
                create_kakakuitem(item_id=2, url_id=2),
            ]
            for item in items:
                await repository.save(item)

            await repository.delete_by_item_id(items[0].item_id)
            ret = await repository.find_by_item_id(items[0].item_id)
            assert ret is None
