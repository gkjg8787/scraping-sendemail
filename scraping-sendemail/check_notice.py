import asyncio
import os
import logging.config


from settings import KAKAKU_NOTICE, LOGGER_CONFIG, NOTICELOG
from application.kakaku_notice import (
    KakakuNotice,
    KakakuNoticeOption,
    KakakuNoticeCommand,
)
from application.noticelog import NoticeLogConfig
from externalfacade.items import KakakuItemFactory, KakakuItemRepository
from externalfacade.kakaku_notice import PreviousDaysKakakuData
from externalfacade.notice import (
    NoticeLogFactory,
    NoticeLogRepository,
    NoticeLogIdentity,
)
from externalfacade import get_async_session

ENV_SENDER_EMAIL = "SOURCE_EMAIL_ADDRESS"
ENV_SENDER_PASSWORD = "SOURCE_EMAIL_PASSWORD"
ENV_RECIPIENT_EMAIL = "DEST_EMAIL_ADDRESS"


async def main():
    logging.config.dictConfig(LOGGER_CONFIG)
    logger = logging.getLogger("kakaku_notice")
    logger.info("start check notice")
    sender_email = os.getenv(ENV_SENDER_EMAIL)
    sender_password = os.getenv(ENV_SENDER_PASSWORD)
    recipient_email = os.getenv(ENV_RECIPIENT_EMAIL)

    if not sender_email or not sender_password or not recipient_email:
        logger.error("enviroment variable is empty")
        return

    async for db in get_async_session():
        command = KakakuNoticeCommand(
            kakaku_url=KAKAKU_NOTICE["kakaku_url"],
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=recipient_email,
            notice_option=KakakuNoticeOption(**KAKAKU_NOTICE["kakaku_notice_option"]),
            kakakuitemfactory=KakakuItemFactory(),
            kakakuitemrepository=KakakuItemRepository(session=db),
            predaysdata=PreviousDaysKakakuData(session=db),
            noticelogfactory=NoticeLogFactory(),
            noticelogrepository=NoticeLogRepository(session=db),
            noticelogidentity=NoticeLogIdentity(session=db),
            noticelogconfig=NoticeLogConfig(**NOTICELOG),
            logger=logger,
        )
        notice = KakakuNotice(kakakunoticecommand=command)
        await notice.execute()

    logger.info("end check notice")


if __name__ == "__main__":
    asyncio.run(main())
