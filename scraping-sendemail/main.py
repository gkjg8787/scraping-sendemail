from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from router.html import admin

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(admin.router)


@app.get("/")
async def root(request: Request):
    return RedirectResponse(
        url=request.url_for("read_admin_noticeloglist"),
        status_code=status.HTTP_302_FOUND,
    )
