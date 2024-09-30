from datetime import datetime

import pytest
import freezegun

from domain.model import NoticeLog, NoticeType
from application.noticelog import NoticeLogOrganizer, NoticeLogConfig
from inmemory.notice import NoticeLogDictRepository

from .shared import create_noticelog


@pytest.mark.asyncio
async def test_NoticeLogOrganizer_no_data(mocker):
    data: dict[int, NoticeLog] = {}
    repo = NoticeLogDictRepository(data=data)
    config = {
        "storagecount": 5,
        "storagedays": 30,
    }
    organizer = NoticeLogOrganizer(
        repository=repo, noticelogconfig=NoticeLogConfig(**config)
    )
    await organizer.execute()
    rets = await repo.find_all()
    assert len(rets) == 0


@pytest.mark.asyncio
async def test_NoticeLogOrganizer_count_max(mocker):
    data: dict[int, NoticeLog] = {
        1: create_noticelog(log_id=1),
        2: create_noticelog(log_id=2),
        3: create_noticelog(log_id=3),
        4: create_noticelog(log_id=4),
        5: create_noticelog(log_id=5),
        6: create_noticelog(log_id=6),
    }
    repo = NoticeLogDictRepository(data=data)
    config = {
        "storagecount": 5,
        "storagedays": 30,
    }
    organizer = NoticeLogOrganizer(
        repository=repo, noticelogconfig=NoticeLogConfig(**config)
    )

    await organizer.execute()
    rets = await repo.find_all()
    assert len(rets) == 5
    ids = [d.log_id for d in rets]
    assert 1 not in ids


@pytest.mark.asyncio
async def test_NoticeLogOrganizer_delete_older_date():
    data: dict[int, NoticeLog] = {
        1: create_noticelog(log_id=1, created_at=datetime(2024, 9, 20)),
        2: create_noticelog(log_id=2, created_at=datetime(2024, 9, 21)),
        3: create_noticelog(log_id=3, created_at=datetime(2024, 9, 22)),
        4: create_noticelog(log_id=4, created_at=datetime(2024, 8, 29)),
        5: create_noticelog(log_id=5, created_at=datetime(2024, 8, 28)),
        6: create_noticelog(log_id=6, created_at=datetime(2024, 9, 28)),
    }
    repo = NoticeLogDictRepository(data=data)
    config = {
        "storagecount": 10,
        "storagedays": 30,
    }
    organizer = NoticeLogOrganizer(
        repository=repo, noticelogconfig=NoticeLogConfig(**config)
    )
    with freezegun.freeze_time("2024-09-28"):
        await organizer.execute()
    rets = await repo.find_all()
    assert len(rets) == 5
    ids = [d.log_id for d in rets]
    assert 5 not in ids
