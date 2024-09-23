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
