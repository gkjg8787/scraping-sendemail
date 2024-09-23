from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class NoticeType(Enum):
    CHECK = 0
    API_CHECK = 1
    UPDATE_NOTICE = 100


class NoticeLog(BaseModel):
    log_id: int
    notice_type: NoticeType
    err_num: int
    text: str
    created_at: datetime
