from pydantic import BaseModel


class NoitceLogGetForm(BaseModel):
    etype: int = 0
    ntype: int = 0

    def __init__(self, etype: str = "", ntype: str = ""):
        super().__init__()
        if etype and etype.isdigit():
            self.etype = int(etype)
        if ntype and ntype.isdigit():
            self.ntype = int(ntype)


class NoticeLogDetailGetForm(BaseModel):
    id: int
