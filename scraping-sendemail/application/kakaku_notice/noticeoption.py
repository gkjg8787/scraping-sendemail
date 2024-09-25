from enum import Enum

from pydantic import BaseModel


class KakakuNoticeOption(BaseModel):
    new_item: bool = True
    remove_item: bool = False
    change_to_in_stock: bool = True
    change_to_out_of_stock: bool = False
    lowest_price: bool = True
    price_decline: bool = True
    price_rise: bool = False
    lowest_price_without_no_change: bool = False


class KakakuNoticeOptionDescription(Enum):
    NEW_ITEM = (1, "new_item", "新規アイテム", "追加されたアイテムの通知")
    REMOVE_ITEM = (2, "remove_item", "削除アイテム", "削除されたアイテムの通知")
    CHANGE_TO_IN_STOCK = (
        11,
        "change_to_in_stock",
        "在庫あり",
        "在庫なしから在庫ありになった通知",
    )
    CHANGE_TO_OUT_OF_STOCK = (
        12,
        "change_to_out_of_stock",
        "在庫なし",
        "在庫ありから在庫なしになった通知",
    )
    LOWEST_PRICE = (21, "lowest_price", "最安値", "最安値の更新通知")
    PRICE_DECLINE = (31, "price_decline", "値段の下落", "値段が下がった通知")
    PRICE_RISE = (32, "price_rise", "値段の上昇", "値段が上がった通知")
    LOWEST_PRICE_WITHOUT_NO_CHANGE = (
        22,
        "lowest_price_without_no_change",
        "最安値（値段変更なし)",
        "値段の変動なしの最安値通知",
    )

    def __init__(self, id: int, qname: str, jname: str, description: str):
        self.id = id
        self.qname = qname
        self.jname = jname
        self.description = description
