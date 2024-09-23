import logging

from pydantic import BaseModel, ConfigDict

from domain.model import (
    IKakakuItemFactory,
    IKakakuItemRepository,
)
from .noticeoption import KakakuNoticeOption
from .previousdaysdata import IPreviousDaysKakakuData
from .writenoticelog import NoticeLogger


class KakakuNoticeCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kakaku_url: str
    sender_email: str
    sender_password: str
    recipient_email: str
    notice_option: KakakuNoticeOption
    kakakuitemfactory: IKakakuItemFactory
    kakakuitemrepository: IKakakuItemRepository
    predaysdata: IPreviousDaysKakakuData
    noticelogger: NoticeLogger
    logger: logging.Logger
