import logging

from pydantic import BaseModel, ConfigDict

from domain.model import (
    IKakakuItemFactory,
    IKakakuItemRepository,
    INoticeLogFactory,
    INoticeLogRepository,
)
from domain.service import INoticeLogIdentity
from .noticeoption import KakakuNoticeOption
from .previousdaysdata import IPreviousDaysKakakuData
from application.noticelog import NoticeLogConfig


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
    noticelogfactory: INoticeLogFactory
    noticelogrepository: INoticeLogRepository
    noticelogidentity: INoticeLogIdentity
    noticelogconfig: NoticeLogConfig
    logger: logging.Logger
