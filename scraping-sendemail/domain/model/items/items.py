from datetime import datetime

from pydantic import BaseModel, field_validator


class KakakuItem(BaseModel):
    item_id: int
    name: str = ""
    url_id: int = -1
    url: str = ""
    price: int = -1
    trendrate: float = 0.0
    salename: str = ""
    storename: str = ""
    updated_at: datetime
    record_low: int = -1
    active_url: int = 0
