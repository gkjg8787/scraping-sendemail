from pydantic import BaseModel


from application.kakaku_notice import KakakuNoticeOption
from application.kakaku_notice.noticeoption import KakakuNoticeOptionDescription
from .shared import htmlcontext, htmlname, htmlelement, util as sutil
from settings import KAKAKU_NOTICE


class NoticeConfigOption(BaseModel):
    name: str
    value: bool
    description: str


class NoticeConfigResult(htmlcontext.HtmlContext):
    options_title: str
    options: list[NoticeConfigOption]


class NoticeConfigResultFactory:
    @classmethod
    def create(
        cls,
        kakakunoticeoption: KakakuNoticeOption,
        options_title: str = "kakakuscraping-fastapiの通知設定",
    ) -> NoticeConfigResult:
        options: list[NoticeConfigOption] = []

        def get_description(key: str):
            for d in KakakuNoticeOptionDescription:
                if d.qname == key:
                    return d.description
            return ""

        for k, v in kakakunoticeoption.model_dump().items():
            option = NoticeConfigOption(name=k, value=v, description=get_description(k))
            options.append(option)
        return NoticeConfigResult(options_title=options_title, options=options)


class NoticeConfigHTML:
    def __init__(self):
        pass

    async def execute(self):
        return NoticeConfigResultFactory.create(
            KakakuNoticeOption(**KAKAKU_NOTICE["kakaku_notice_option"])
        )
