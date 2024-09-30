import os
from datetime import datetime

from application.kakaku_notice.parse import KakakuParser
from domain.model import KakakuItem
from externalfacade.items import KakakuItemFactory

no_data_fpath = os.path.dirname(__file__) + "/data/no_data.html"
three_data_fpath = os.path.dirname(__file__) + "/data/three_data.html"
sinagire_shokai_fpath = os.path.dirname(__file__) + "/data/sinagire_syokai_data.html"


def test_KakakuParser_no_data():
    with open(no_data_fpath, encoding="utf-8") as fp:
        parser = KakakuParser(fp, kakakuitemfactory=KakakuItemFactory())
        assert not parser.results


def convert_datetime(datetime_str: str) -> datetime:
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(datetime_str, format)


def test_KakakuParser_three_data():
    correct_data = {
        "1": {
            "item_id": 1,
            "name": "天空の城ラピュタ",
            "url_id": 2,
            "url": "https://www.suruga-ya.jp/product/other/728006800",
            "price": 2350,
            "trendrate": 0.0,
            "salename": "",
            "storename": "駿河屋",
            "updated_at": convert_datetime("2024-09-18 15:12:42"),
            "record_low": 2350,
            "active_url": 2,
        },
        "2": {
            "item_id": 2,
            "name": "となりのトトロ",
            "url_id": 3,
            "url": "https://www.suruga-ya.jp/product/other/128002938",
            "price": 2430,
            "trendrate": 0.0,
            "salename": "",
            "storename": "駿河屋",
            "updated_at": convert_datetime("2024-09-18 15:12:44"),
            "record_low": 2430,
            "active_url": 1,
        },
        "3": {
            "item_id": 3,
            "name": "耳をすませば",
            "url_id": 4,
            "url": "https://www.suruga-ya.jp/product/other/128004530",
            "price": 2640,
            "trendrate": 0.0,
            "salename": "",
            "storename": "駿河屋新潟駅南店",
            "updated_at": convert_datetime("2024-09-18 15:12:46"),
            "record_low": 2640,
            "active_url": 2,
        },
    }
    parser = None
    with open(three_data_fpath, encoding="utf-8") as fp:
        parser = KakakuParser(fp, kakakuitemfactory=KakakuItemFactory())
    assert parser is not None
    assert len(parser.results) == 3
    for r in parser.results:
        assert r.model_dump() == correct_data[str(r.item_id)]


def test_KakakuParser_sinagire_syokai():
    correct_data = {
        "1": {
            "item_id": 1,
            "name": "ゼノブレイドクロス セット(WiiU本体同梱)(状態：HDMIケーブル欠品)",
            "url_id": -1,
            "url": "",
            "price": -1,
            "trendrate": 0.0,
            "salename": "",
            "storename": "",
            "updated_at": convert_datetime("2024-09-29 23:24:24"),
            "record_low": -1,
            "active_url": 1,
        }
    }
    parser = None
    with open(sinagire_shokai_fpath, encoding="utf-8") as fp:
        parser = KakakuParser(fp, kakakuitemfactory=KakakuItemFactory())
    assert parser is not None
    assert len(parser.results) == 1
    for r in parser.results:
        assert r.model_dump() == correct_data[str(r.item_id)]
