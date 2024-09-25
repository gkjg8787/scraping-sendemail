from datetime import datetime, tzinfo, timezone

from domain.model import NoticeLog, INoticeLogRepository, NoticeType
from application.kakaku_notice import ErrNumFilter, NoticeTypeFilter
from router.html.param import NoitceLogGetForm
from .shared import htmlcontext, htmlname, htmlelement, util as sutil


class ErrFilterFacotry:
    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "エラーフィルタ",
        input_name: str = htmlname.GETNAME.ETYPE.value,
        select_id: int = 0,
    ) -> htmlelement.SelectForm:
        menu_list: list[htmlelement.SelectOption] = []
        for s in ErrNumFilter:
            selectopt = htmlelement.SelectOption(id=s.id, text=s.jname, selected="")
            if select_id == s.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlelement.SelectForm(
            form=htmlelement.Form(method=form_method, action=form_action),
            select=htmlelement.Select(
                title=title, input_name=input_name, menu_list=menu_list
            ),
        )


class NoticeTypeFilterFacotry:
    @classmethod
    def create(
        cls,
        form_method: str = htmlname.FORMMETHOD.GET.value,
        form_action: str = "",
        title: str = "動作種別",
        input_name: str = htmlname.GETNAME.NTYPE.value,
        select_id: int = 0,
    ) -> htmlelement.SelectForm:
        menu_list: list[htmlelement.SelectOption] = []
        for s in NoticeTypeFilter:
            selectopt = htmlelement.SelectOption(id=s.id, text=s.jname, selected="")
            if select_id == s.id:
                selectopt.selected = htmlname.HTMLTemplateValue.SELECTED
            menu_list.append(selectopt)
        return htmlelement.SelectForm(
            form=htmlelement.Form(method=form_method, action=form_action),
            select=htmlelement.Select(
                title=title, input_name=input_name, menu_list=menu_list
            ),
        )


class NoticeLogListResult(htmlcontext.HtmlContext):
    err_filter: htmlelement.SelectForm
    noticetype_filter: htmlelement.SelectForm
    hidden_input_dict: dict
    noticelogs: list[NoticeLog] = []
    noticelogs_length: int = 0
    error_msg: str = ""
    PARAM_ID: str = htmlname.POSTNAME.ID.value


class NoticeLogListResultFactory:
    @classmethod
    def create(
        cls,
        noticeloggetform: NoitceLogGetForm,
        noticelogs: list[dict],
        error_msg: str = "",
        local_timezone: tzinfo | None = None,
    ) -> NoticeLogListResult:
        noticelogs_length = len(noticelogs)
        hidden_input_dict = {}
        if noticeloggetform.etype:
            hidden_input_dict["etype"] = noticeloggetform.etype
        if noticeloggetform.ntype:
            hidden_input_dict["ntype"] = noticeloggetform.ntype
        if noticelogs:
            noticelogs = cls.create_noticelogs(noticelogs, tz=local_timezone)
        return NoticeLogListResult(
            err_filter=ErrFilterFacotry.create(select_id=noticeloggetform.etype or 0),
            noticetype_filter=NoticeTypeFilterFacotry.create(
                select_id=noticeloggetform.ntype or 0
            ),
            hidden_input_dict=hidden_input_dict,
            noticelogs=noticelogs,
            noticelogs_length=noticelogs_length,
            error_msg=error_msg,
        )

    @classmethod
    def create_noticelogs(cls, logs: list[dict], tz: tzinfo) -> list[NoticeLog]:
        results: list[NoticeLog] = []
        now = datetime.now(timezone.utc)
        for i in logs:
            noticelog = NoticeLog(**i)
            results.append(noticelog)
            cls.toLocaltimezone(noticelog, tz=tz)
        return results

    @classmethod
    def toLocaltimezone(cls, log: NoticeLog, tz: tzinfo) -> None:
        log.created_at = sutil.utcTolocaltime(input_date=log.created_at, tz=tz)


class NoticeLogListHTML:
    noticeloggetform: NoitceLogGetForm
    local_timezone: tzinfo
    repository: INoticeLogRepository

    def __init__(
        self,
        noticeloggetform: NoitceLogGetForm,
        local_timezone: tzinfo,
        repository: INoticeLogRepository,
    ):
        self.noticeloggetform = noticeloggetform
        self.local_timezone = local_timezone
        self.repository = repository

    async def execute(self) -> NoticeLogListResult:
        input_list: list[NoticeLog] = []
        err_num = None
        notice_type = None
        target_date = None
        keyword = None
        if self.noticeloggetform.etype:
            match self.noticeloggetform.etype:
                case ErrNumFilter.ALL.id:
                    err_num = None
                case ErrNumFilter.ERROR_ONLY.id:
                    err_num = 1
                case ErrNumFilter.NON_ERROR.id:
                    err_num = 0
        if self.noticeloggetform.ntype:
            match self.noticeloggetform.ntype:
                case NoticeTypeFilter.ALL.id:
                    notice_type = None
                case NoticeTypeFilter.CHECK.id:
                    notice_type = NoticeType.CHECK
                case NoticeTypeFilter.API_CHECK.id:
                    notice_type = NoticeType.API_CHECK
                case NoticeTypeFilter.UPDATE_NOTICE.id:
                    notice_type = NoticeType.UPDATE_NOTICE
        input_list = await self.repository.find_by_filter(
            notice_type=notice_type,
            err_num=err_num,
            target_date=target_date,
            keyword=keyword,
        )
        input_dict = [nl.model_dump() for nl in reversed(input_list)]
        return NoticeLogListResultFactory.create(
            noticeloggetform=self.noticeloggetform,
            noticelogs=input_dict,
            local_timezone=self.local_timezone,
        )
