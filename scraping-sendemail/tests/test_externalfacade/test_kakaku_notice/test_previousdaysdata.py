from datetime import datetime, timedelta

import pytest

from externalfacade.items import KakakuItemRepository
from externalfacade.kakaku_notice import PreviousDaysKakakuData

from tests.test_externalfacade.shared import create_kakakuitem, JST, compare_kakakuitem


class TestPreviousDaysKakakuData:
    @pytest.mark.asyncio
    async def test_get(self, test_db):
        async for db in test_db:
            items = [
                create_kakakuitem(item_id=1, url_id=1, updated_at=datetime.now(JST)),
                create_kakakuitem(
                    item_id=2,
                    url_id=2,
                    updated_at=datetime.now(JST) - timedelta(days=1),
                ),
            ]
            repository = KakakuItemRepository(session=db)
            for item in items:
                await repository.save(item)
            previousdays = PreviousDaysKakakuData(session=db)
            results = await previousdays.get()
            assert len(results) == 1
            assert compare_kakakuitem(results[0], items[1])
