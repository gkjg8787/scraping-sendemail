from domain.model import KakakuItem
from .noticeoption import KakakuNoticeOption


class ConstValue:
    INIT_PRICE = -1
    NONE_ID = -1


class ComparisionResult:
    new_items: list[KakakuItem]
    remove_items: list[KakakuItem]
    change_to_in_stock_items: list[KakakuItem]
    change_to_out_of_stock_items: list[KakakuItem]
    lowest_price_items: list[KakakuItem]
    lowest_price_without_no_change_items: list[KakakuItem]
    price_decline_items: list[KakakuItem]
    price_rise_items: list[KakakuItem]

    def __init__(self):
        self.new_items = []
        self.remove_items = []
        self.change_to_in_stock_items = []
        self.change_to_out_of_stock_items = []
        self.lowest_price_items = []
        self.lowest_price_without_no_change_items = []
        self.price_decline_items = []
        self.price_rise_items = []

    def create_message(self) -> str:
        head_text_list = [
            "【本日の更新の通知】\n",
            "format : アイテムID, アイテム名, 価格, 前日比, 店舗名, 今までの最安値\n",
        ]
        body_text_list: list[str] = []

        def body_append(value: str):
            body_text_list.append(value)
            body_text_list.append("\n")

        if self.new_items:
            new_t = "■新規追加されたアイテム" + "\n"
            for item in self.new_items:
                new_t += self.convert_to_email_format(item) + "\n"
            body_append(new_t)

        if self.remove_items:
            remove_t = "■削除されたアイテム" + "\n"
            for item in self.remove_items:
                remove_t += self.convert_to_email_format(item) + "\n"
            body_append(remove_t)

        if self.change_to_in_stock_items:
            in_stock_t = "■在庫ありになったアイテム" + "\n"
            for item in self.change_to_in_stock_items:
                in_stock_t += self.convert_to_email_format(item) + "\n"
            body_append(in_stock_t)

        if self.change_to_out_of_stock_items:
            out_of_stock_t = "■在庫なしになったアイテム" + "\n"
            for item in self.change_to_out_of_stock_items:
                out_of_stock_t += self.convert_to_email_format(item) + "\n"
            body_append(out_of_stock_t)

        if self.lowest_price_items:
            lowest_price_t = "■最安値が更新されたアイテム" + "\n"
            for item in self.lowest_price_items:
                lowest_price_t += self.convert_to_email_format(item) + "\n"
            body_append(lowest_price_t)

        if self.lowest_price_without_no_change_items:
            lowest_price_without_no_change_t = "■最安値を維持しているアイテム" + "\n"
            for item in self.lowest_price_without_no_change_items:
                lowest_price_without_no_change_t += (
                    self.convert_to_email_format(item) + "\n"
                )
            body_append(lowest_price_without_no_change_t)

        if self.price_decline_items:
            price_decline_t = "■値段が下がったアイテム" + "\n"
            for item in self.price_decline_items:
                price_decline_t += self.convert_to_email_format(item) + "\n"
            body_append(price_decline_t)

        if self.price_rise_items:
            price_rise_t = "■値段が上がったアイテム" + "\n"
            for item in self.price_rise_items:
                price_rise_t += self.convert_to_email_format(item) + "\n"
            body_append(price_rise_t)

        if not body_text_list:
            return ""

        result = "\n".join(head_text_list + body_text_list)
        return result

    def convert_to_email_format(self, item: KakakuItem) -> str:
        return f"{item.item_id}, {item.name}, {item.price}, {item.trendrate}%, {item.storename}, {item.record_low}"


class KakakuDataComparision:
    notice_option: KakakuNoticeOption

    def __init__(self, notice_option: KakakuNoticeOption):
        self.notice_option = notice_option

    def execute(
        self, new_data: list[KakakuItem], old_data: list[KakakuItem]
    ) -> ComparisionResult:
        result = ComparisionResult()
        notice_option: KakakuNoticeOption = self.notice_option

        if notice_option.new_item or notice_option.remove_item:
            new_ids = {item.item_id for item in new_data}
            old_ids = {item.item_id for item in old_data}

            uniq_to_new = new_ids - old_ids
            uniq_to_old = old_ids - new_ids

            if notice_option.new_item:
                uniq_items_new = [
                    item for item in new_data if item.item_id in uniq_to_new
                ]
                result.new_items.extend(uniq_items_new)
            if notice_option.remove_item:
                uniq_items_old = [
                    item for item in old_data if item.item_id in uniq_to_old
                ]
                result.remove_items.extend(uniq_items_old)

        for new in new_data:
            for old in old_data:
                if new.item_id != old.item_id:
                    continue
                if notice_option.change_to_in_stock:
                    if (
                        old.price == ConstValue.INIT_PRICE
                        and new.price != ConstValue.INIT_PRICE
                    ):
                        result.change_to_in_stock_items.append(new)
                if notice_option.change_to_out_of_stock:
                    if (
                        old.price != ConstValue.INIT_PRICE
                        and new.price == ConstValue.INIT_PRICE
                    ):
                        result.change_to_out_of_stock_items.append(new)
                if notice_option.lowest_price:
                    if (
                        new.price != ConstValue.INIT_PRICE
                        and old.record_low != ConstValue.INIT_PRICE
                        and old.record_low > new.price
                    ):
                        result.lowest_price_items.append(new)
                if notice_option.lowest_price_without_no_change:
                    if (
                        new.price != ConstValue.INIT_PRICE
                        and old.record_low != ConstValue.INIT_PRICE
                        and old.record_low == new.price
                        and old.price == new.price
                    ):
                        result.lowest_price_without_no_change_items.append(new)
                if notice_option.price_decline:
                    if new.price != ConstValue.INIT_PRICE and new.price < old.price:
                        result.price_decline_items.append(new)
                if notice_option.price_rise:
                    if old.price != ConstValue.INIT_PRICE and new.price > old.price:
                        result.price_rise_items.append(new)

        return result
