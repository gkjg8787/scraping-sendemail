from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from fastapi.templating import Jinja2Templates


from sqlalchemy.ext.asyncio import AsyncSession

from externalfacade import get_async_session
from .param import NoitceLogGetForm, NoticeLogDetailGetForm
from .usecase import NoticeLogListHTML, NoticeLogHTML, NoticeConfigHTML
from .usecase.shared import util
from externalfacade.notice import NoticeLogRepository


router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")
templates.env.filters["toLocalTextFormat"] = util.toLocalTextFormat


@router.get("/log", response_class=HTMLResponse)
async def read_admin_noticeloglist(
    request: Request,
    noticeloggetform: NoitceLogGetForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await NoticeLogListHTML(
        noticeloggetform=noticeloggetform,
        local_timezone=util.JST,
        repository=NoticeLogRepository(db),
    ).execute()
    ret = templates.TemplateResponse(
        request=request, name="admin/noticeloglist.html", context=result.get_context()
    )
    return ret


@router.get("/log/detail", response_class=HTMLResponse)
async def read_admin_noticelogdetail(
    request: Request,
    noticelogdetailgetform: NoticeLogDetailGetForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await NoticeLogHTML(
        log_id=noticelogdetailgetform.id,
        local_timezone=util.JST,
        repository=NoticeLogRepository(db),
    ).execute()
    ret = templates.TemplateResponse(
        request=request, name="admin/noticelogdetail.html", context=result.get_context()
    )
    return ret


@router.get("/config", response_class=HTMLResponse)
async def read_admin_viewconfig(
    request: Request,
):
    result = await NoticeConfigHTML().execute()
    ret = templates.TemplateResponse(
        request=request, name="admin/noticeconfig.html", context=result.get_context()
    )
    return ret
