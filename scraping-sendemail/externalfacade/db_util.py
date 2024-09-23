from sqlalchemy import URL, create_engine

from settings import DATABASES
from .items import items
from .notice import notice

dbconf = DATABASES
url_obj = URL.create(**dbconf["default"])
is_echo = dbconf["is_echo"]
engine = create_engine(url_obj, echo=is_echo)


def create_db():
    items.Base.metadata.create_all(engine)
    notice.Base.metadata.create_all(engine)


def remove_db():
    items.Base.metadata.drop_all(engine)
    notice.Base.metadata.drop_all(engine)
