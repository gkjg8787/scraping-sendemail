from application.kakaku_notice import KakakuNoticeOption
from application.kakaku_notice.comparision import (
    KakakuDataComparision,
    ComparisionResult,
)

from .shared import create_kakakuitem


def equal_ComparisionResult(one: ComparisionResult, two: ComparisionResult) -> bool:
    if one.new_items != two.new_items:
        return False
    if one.remove_items != two.remove_items:
        return False
    if one.change_to_in_stock_items != two.change_to_in_stock_items:
        return False
    if one.change_to_out_of_stock_items != two.change_to_out_of_stock_items:
        return False
    if one.lowest_price_items != two.lowest_price_items:
        return False
    if (
        one.lowest_price_without_no_change_items
        != two.lowest_price_without_no_change_items
    ):
        return False
    if one.price_decline_items != two.price_decline_items:
        return False
    if one.price_rise_items != two.price_rise_items:
        return False

    return True


def test_KakakuDataComparision_no_new_no_old():
    comparision = KakakuDataComparision(notice_option=KakakuNoticeOption())
    correct_data = ComparisionResult()
    result = comparision.execute(new_data=[], old_data=[])
    assert equal_ComparisionResult(correct_data, result)


def create_all_noticeoption():
    return KakakuNoticeOption(
        new_item=True,
        remove_item=True,
        change_to_in_stock=True,
        change_to_out_of_stock=True,
        lowest_price=True,
        price_decline=True,
        price_rise=True,
        lowest_price_without_no_change=True,
    )


def test_kakakuDataComparision_no_old():
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    correct_data = ComparisionResult()
    correct_data.new_items = [n for n in new_data]
    comparision = KakakuDataComparision(notice_option=create_all_noticeoption())
    result = comparision.execute(new_data=new_data, old_data=[])
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_no_new():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    correct_data = ComparisionResult()
    correct_data.remove_items = [n for n in old_data]
    comparision = KakakuDataComparision(notice_option=create_all_noticeoption())
    result = comparision.execute(new_data=[], old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_change_to_in_stock():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=-1,
            record_low=-1,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    correct_data.change_to_in_stock_items = [new_data[0]]
    comparision = KakakuDataComparision(notice_option=create_all_noticeoption())
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_change_to_in_stock_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=-1,
            record_low=-1,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.change_to_in_stock = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_change_to_out_of_stock():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=-1,
            record_low=1000,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    correct_data.change_to_out_of_stock_items = [new_data[0]]
    notice_option = create_all_noticeoption()
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_change_to_out_of_stock_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=-1,
            record_low=1000,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.change_to_out_of_stock = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_lowest_price():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=900,
            record_low=900,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    correct_data.lowest_price_items = [new_data[0]]
    # correct_data.price_decline_items = [new_data[0]]
    notice_option = create_all_noticeoption()
    notice_option.price_decline = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_lowest_price_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=900,
            record_low=900,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.lowest_price = False
    notice_option.price_decline = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_lowest_price_without_no_change():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [old for old in old_data]
    correct_data = ComparisionResult()
    correct_data.lowest_price_without_no_change_items = [old_data[0]]
    comparision = KakakuDataComparision(notice_option=create_all_noticeoption())
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_lowest_price_without_no_change_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [old for old in old_data]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.lowest_price_without_no_change = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_price_decline():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=500,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=900,
            record_low=500,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    correct_data.price_decline_items = [new_data[0]]
    notice_option = create_all_noticeoption()
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_price_decline_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=500,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=900,
            record_low=500,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.price_decline = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_price_rise():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=500,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1100,
            record_low=500,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    correct_data.price_rise_items = [new_data[0]]
    notice_option = create_all_noticeoption()
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_price_rise_options_off():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=500,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1100,
            record_low=500,
            storename="storeA",
        ),
        old_data[1],
    ]
    correct_data = ComparisionResult()
    notice_option = create_all_noticeoption()
    notice_option.price_rise = False
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_lowest_and_price_decline():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
        create_kakakuitem(
            item_id=3,
            name="item03",
            url_id=3,
            price=3000,
            record_low=1500,
            storename="storeC",
        ),
        create_kakakuitem(
            item_id=4,
            name="item04",
            url_id=4,
            price=1700,
            record_low=1500,
            storename="storeD",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=500,
            record_low=500,
            storename="storeA",
        ),
        old_data[1],
        create_kakakuitem(
            item_id=3,
            name="item03",
            url_id=3,
            price=2100,
            record_low=1500,
            storename="storeC",
        ),
        create_kakakuitem(
            item_id=4,
            name="item04",
            url_id=4,
            price=1400,
            record_low=1400,
            storename="storeD",
        ),
    ]
    correct_data = ComparisionResult()
    correct_data.lowest_price_items = [new_data[0], new_data[3]]
    correct_data.price_decline_items = [new_data[0], new_data[2], new_data[3]]
    notice_option = create_all_noticeoption()
    comparision = KakakuDataComparision(notice_option=notice_option)
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()


def test_KakakuDataComparision_change_to_in_stock_and_lowest():
    old_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=-1,
            record_low=1200,
            storename="storeA",
        ),
        create_kakakuitem(
            item_id=2,
            name="item02",
            url_id=2,
            price=2000,
            record_low=1500,
            storename="storeB",
        ),
        create_kakakuitem(
            item_id=3,
            name="item03",
            url_id=3,
            price=-1,
            record_low=5000,
            storename="storeC",
        ),
    ]
    new_data = [
        create_kakakuitem(
            item_id=1,
            name="item01",
            url_id=1,
            price=1000,
            record_low=1000,
            storename="storeA",
        ),
        old_data[1],
        create_kakakuitem(
            item_id=3,
            name="item03",
            url_id=3,
            price=5500,
            record_low=5000,
            storename="storeC",
        ),
    ]
    correct_data = ComparisionResult()
    correct_data.lowest_price_items = [new_data[0]]
    correct_data.change_to_in_stock_items = [new_data[0], new_data[2]]
    comparision = KakakuDataComparision(notice_option=create_all_noticeoption())
    result = comparision.execute(new_data=new_data, old_data=old_data)
    assert equal_ComparisionResult(correct_data, result)
    assert correct_data.create_message() == result.create_message()
