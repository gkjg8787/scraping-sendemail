import pytest

from application.kakaku_notice.kakaku_notice import KakakuCheckAndMessageCreator
from application.kakaku_notice import KakakuNoticeOption
from application.kakaku_notice.comparision import ComparisionResult
from inmemory.items import KakakuItemFactory, KakakuItemDictRepository
from inmemory.kakaku_notice import PreviousDaysDictKakakuData
from domain.model import KakakuItem

from .test_parse import no_data_fpath, three_data_fpath


@pytest.mark.asyncio
async def test_KakakuCheckAndMessageCreator_get_no_data(mocker):
    m = mocker.patch(
        "application.kakaku_notice.kakaku_notice.KakakuCheckAndMessageCreator.get_html"
    )
    with open(no_data_fpath, encoding="utf-8") as f:
        html_text = f.read()
    m.return_value = html_text

    data: dict[int, KakakuItem] = {}
    msgcreator = KakakuCheckAndMessageCreator(
        kakaku_url="xxx",
        kakakuitemfactory=KakakuItemFactory(),
        kakakuitemrepository=KakakuItemDictRepository(data=data),
        notice_option=KakakuNoticeOption(),
        predaysdata=PreviousDaysDictKakakuData(data=data),
    )
    ret = await msgcreator.get_message()
    assert len(ret) == 0


@pytest.mark.asyncio
async def test_KakakuCheckAndMessageCreator_get_message(mocker):
    m = mocker.patch(
        "application.kakaku_notice.kakaku_notice.KakakuCheckAndMessageCreator.get_html"
    )
    with open(three_data_fpath, encoding="utf-8") as f:
        html_text = f.read()
    m.return_value = html_text

    data: dict[int, KakakuItem] = {}
    msgcreator = KakakuCheckAndMessageCreator(
        kakaku_url="xxx",
        kakakuitemfactory=KakakuItemFactory(),
        kakakuitemrepository=KakakuItemDictRepository(data=data),
        notice_option=KakakuNoticeOption(),
        predaysdata=PreviousDaysDictKakakuData(data=data),
    )
    ret = await msgcreator.get_message()
    assert ret
    assert len(data) == 3
    comparision = ComparisionResult()
    comparision.new_items = [kakaku for kakaku in data.values()]
    assert comparision.create_message() == ret
