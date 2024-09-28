from pydantic import BaseModel


class NoticeLogConfig(BaseModel):
    storagecount: int
    storagedays: int
