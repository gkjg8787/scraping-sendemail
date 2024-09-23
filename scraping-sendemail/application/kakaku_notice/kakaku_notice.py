from datetime import datetime
from zoneinfo import ZoneInfo

from domain.model import (
    IKakakuItemFactory,
    IKakakuItemRepository,
    KakakuItem,
    INoticeLogFactory,
    INoticeLogRepository,
    NoticeLog,
    NoticeType,
)
from application.sendemail import OneMailCreator, EmailSender, Async_MessageCreator
from application.download import DownloadCommand, DownloadType, async_download_text

from .parse import KakakuParser
from .noticeoption import KakakuNoticeOption
from .previousdaysdata import IPreviousDaysKakakuData
from .comparision import KakakuDataComparision
from .command import KakakuNoticeCommand

JST = ZoneInfo("Asia/Tokyo")


class KakakuCheckAndMessageCreator(Async_MessageCreator):
    kakaku_url: str
    kakakuitemfacotry: IKakakuItemFactory
    kakakuitemrepository: IKakakuItemRepository
    predaysdata: IPreviousDaysKakakuData
    notice_option: KakakuNoticeOption

    def __init__(
        self,
        kakaku_url: str,
        kakakuitemfactory: IKakakuItemFactory,
        kakakuitemrepository: IKakakuItemRepository,
        notice_option: KakakuNoticeOption,
        predaysdata: IPreviousDaysKakakuData,
    ):
        self.kakaku_url = kakaku_url
        self.kakakuitemfacotry = kakakuitemfactory
        self.kakakuitemrepository = kakakuitemrepository
        self.notice_option = notice_option
        self.predaysdata = predaysdata

    async def get_message(self) -> str:
        text = await self.get_html()
        parser = KakakuParser(htmltext=text, kakakuitemfactory=self.kakakuitemfacotry)
        predata = await self.predaysdata.get()
        if not predata:
            predata = await self.kakakuitemrepository.find_all() or []
        kakakucomparision = KakakuDataComparision(notice_option=self.notice_option)
        comparisionresult = kakakucomparision.execute(
            new_data=parser.results, old_data=predata
        )
        await self.data_update(new_data=parser.results, old_data=predata)
        return comparisionresult.create_message()

    async def get_html(self) -> str:
        result = await async_download_text(
            DownloadCommand(url=self.kakaku_url, downloadtype=DownloadType.GET)
        )
        return result

    async def data_update(self, new_data: list[KakakuItem], old_data: list[KakakuItem]):
        repository = self.kakakuitemrepository
        new_ids = {item.item_id for item in new_data}
        old_ids = {item.item_id for item in old_data}

        uniq_to_old = old_ids - new_ids

        for old_id in uniq_to_old:
            await repository.delete_by_item_id(item_id=old_id)

        for new in new_data:
            await repository.save(new)

        return


class KakakuNotice:
    kakakunoticecommand: KakakuNoticeCommand

    def __init__(self, kakakunoticecommand: KakakuNoticeCommand):
        self.kakakunoticecommand = kakakunoticecommand

    async def execute(self):
        command: KakakuNoticeCommand = self.kakakunoticecommand
        mailcreator = OneMailCreator(
            [
                KakakuCheckAndMessageCreator(
                    kakaku_url=command.kakaku_url,
                    kakakuitemfactory=command.kakakuitemfactory,
                    kakakuitemrepository=command.kakakuitemrepository,
                    notice_option=command.notice_option,
                    predaysdata=command.predaysdata,
                )
            ]
        )
        try:
            text = await mailcreator.execute()
        except Exception as e:
            await command.noticelogger.check(err_num=1, text=str(e))
            return
        await command.noticelogger.check()
        if text:
            command.logger.info("send email")
            try:
                EmailSender.send_email(
                    sender_email=command.sender_email,
                    sender_password=command.sender_password,
                    recipient_email=command.recipient_email,
                    subject=self.get_subject(),
                    message=text,
                )
            except Exception as e:
                await command.noticelogger.update_notice(text=str(e), err_num=1)
                return
            await command.noticelogger.update_notice(text=text)

    def get_subject(self) -> str:
        now = datetime.now(JST)
        result = f"{str(now.date())}の更新通知"
        return result
