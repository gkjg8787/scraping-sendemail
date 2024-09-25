from enum import Enum

from domain.model import NoticeType


class ErrNumFilter(Enum):
    ALL = (1, "全て")
    ERROR_ONLY = (2, "エラーのみ")
    NON_ERROR = (3, "エラーなし")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text


class NoticeTypeFilter(Enum):
    ALL = (0, "全て")
    CHECK = (1, "確認")
    API_CHECK = (2, "APIからの確認")
    UPDATE_NOTICE = (3, "更新通知")

    def __init__(self, id: int, text: str):
        self.id = id
        self.ename = self.name.lower()
        self.jname = text
