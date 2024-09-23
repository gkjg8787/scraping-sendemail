from datetime import datetime

from sqlalchemy import func

INTERVAL_YESTERDAY = -1


def get_jst_datetime_for_query(
    interval_days: int | None = None, interval_years: int | None = None
):
    jst_base: int = 9
    if interval_days is None:
        ret = func.datetime("now", f"{jst_base} hours")
    else:
        interval_jst = jst_base + interval_days * 24
        ret = func.datetime("now", f"{interval_jst} hours")
    if interval_years is None:
        return ret
    return func.datetime(ret, f"{interval_years} years")


def get_jst_date_for_query(
    interval_days: int | None = None, interval_years: int | None = None
):
    return func.date(
        get_jst_datetime_for_query(
            interval_days=interval_days, interval_years=interval_years
        )
    )
