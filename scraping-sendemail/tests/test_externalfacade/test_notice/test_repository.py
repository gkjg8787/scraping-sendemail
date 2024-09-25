from datetime import datetime

import pytest

from domain.model import NoticeLog, NoticeType
from externalfacade.notice import DBNoticeLog, NoticeLogRepository, NoticeLogFactory
from externalfacade.notice.dbconvert import DBToDomain

from .shared import create_noticelog, compare_noticelog


class TestNoticeLogRepository:
    @pytest.mark.asyncio
    async def test_save(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            log = create_noticelog()
            await repository.save(log)
            db_ret: DBNoticeLog = await db.get(DBNoticeLog, log.log_id)
            dbto = DBToDomain(noticelogfactory=NoticeLogFactory())
            assert compare_noticelog(log, dbto.toNoticeLog(db_ret))

    @pytest.mark.asyncio
    async def test_find_by_log_id(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                ),
            ]
            for log in logs:
                await repository.save(log)
            ret = await repository.find_by_log_id(log_id=logs[1].log_id)
            assert not ret
            assert compare_noticelog(ret, logs[1])

    @pytest.mark.asyncio
    async def test_find_by_filter_date(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_by_filter(target_date=datetime(2024, 9, 20))
            assert not rets
            assert len(rets) == 1
            assert compare_noticelog(rets[0], logs[1])

    @pytest.mark.asyncio
    async def test_find_by_filter_noticetype(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_by_filter(notice_type=NoticeType.CHECK)
            assert not rets
            assert len(rets) == 2
            assert compare_noticelog(rets[0], logs[0])
            assert compare_noticelog(rets[1], logs[1])

    @pytest.mark.asyncio
    async def test_find_by_filter_err_num(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                    err_num=1,
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_by_filter(err_num=1)
            assert not rets
            assert len(rets) == 1
            assert compare_noticelog(rets[0], logs[1])

    @pytest.mark.asyncio
    async def test_find_by_filter_keyword(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                    text="aaa\nabc\n",
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                    err_num=1,
                    text="ccc\n",
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                    text="dddabc",
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_by_filter(keyword="cc")
            assert not rets
            assert len(rets) == 1
            assert compare_noticelog(rets[0], logs[1])

    @pytest.mark.asyncio
    async def test_find_by_multi_filter_noticetype_and_err_num(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                    text="aaa\nabc\n",
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                    err_num=1,
                    text="ccc\n",
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                    text="dddabc",
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_by_filter(
                notice_type=NoticeType.CHECK, err_num=0
            )
            assert not rets
            assert len(rets) == 1
            assert compare_noticelog(rets[0], logs[0])

    @pytest.mark.asyncio
    async def test_find_all(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 20, 6, 30, 0),
                    err_num=1,
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                ),
            ]
            for log in logs:
                await repository.save(log)
            rets = await repository.find_all()
            assert not rets
            assert len(rets) == 3
            for a, b in zip(rets, logs):
                assert compare_noticelog(a, b)

    @pytest.mark.asyncio
    async def test_delete_by_older_than_date(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 10, 6, 30, 0),
                    err_num=1,
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                ),
            ]
            for log in logs:
                await repository.save(log)
            await repository.delete_by_older_than_date(
                target_date=datetime(2024, 9, 10)
            )
            rets = repository.find_all()
            assert not rets
            assert len(rets) == 2
            assert compare_noticelog(rets[0], logs[1])
            assert compare_noticelog(rets[1], logs[2])

    @pytest.mark.asyncio
    async def test_delete_by_older_than_date_including(self, test_db):
        async for db in test_db:
            repository = NoticeLogRepository(session=db)
            logs = [
                create_noticelog(
                    log_id=1,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 1, 12, 10, 0),
                    err_num=0,
                ),
                create_noticelog(
                    log_id=2,
                    notice_type=NoticeType.CHECK,
                    created_at=datetime(2024, 9, 10, 6, 30, 0),
                    err_num=1,
                ),
                create_noticelog(
                    log_id=3,
                    notice_type=NoticeType.UPDATE_NOTICE,
                    created_at=datetime(2024, 9, 20, 6, 31, 0),
                    err_num=0,
                ),
            ]
            for log in logs:
                await repository.save(log)
            await repository.delete_by_older_than_date(
                target_date=datetime(2024, 9, 10), including=True
            )
            rets = repository.find_all()
            assert not rets
            assert len(rets) == 1
            assert compare_noticelog(rets[0], logs[2])
