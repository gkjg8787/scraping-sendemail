from domain.model import NoticeLog, INoticeLogFactory, NoticeType
from .notice import DBNoticeLog


class DBToDomain:
    noticelogfactory: INoticeLogFactory

    def __init__(self, noticelogfactory: INoticeLogFactory):
        self.noticelogfactory = noticelogfactory

    def toNoticeLog(self, dbnoticelog: DBNoticeLog) -> NoticeLog:
        for nt in NoticeType:
            if nt.value == int(dbnoticelog.notice_type):
                convert_notice_type = nt
                break
        return self.noticelogfactory.create(
            log_id=dbnoticelog.log_id,
            notice_type=convert_notice_type,
            text=dbnoticelog.text,
            err_num=dbnoticelog.err_num,
            created_at=dbnoticelog.created_at,
        )


class DomainToDB:
    @classmethod
    def toDBNoticeLog(self, noticelog: NoticeLog) -> DBNoticeLog:
        return DBNoticeLog(
            log_id=noticelog.log_id,
            notice_type=str(noticelog.notice_type.value),
            text=noticelog.text,
            err_num=noticelog.err_num,
            created_at=noticelog.created_at,
        )
