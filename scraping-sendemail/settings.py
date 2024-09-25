from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    "default": {
        "drivername": "sqlite",
        "database": f"{BASE_DIR}/db/sendemail.sqlite",
    },
    "default-async": {
        "drivername": "sqlite+aiosqlite",
        "database": f"{BASE_DIR}/db/sendemail.sqlite",
    },
    "is_echo": False,
}

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "precise": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "precise",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "precise",
            "filename": "notice.log",
            "maxBytes": 1024,
            "backupCount": 3,
        },
    },
    "loggers": {
        "kakaku_notice": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}

KAKAKU_NOTICE = {
    "kakaku_url": "your_kakakuscraping-fastapi_users_url",
    "kakaku_notice_option": {
        "new_item": True,
        "remove_item": False,
        "change_to_in_stock": True,
        "change_to_out_of_stock": False,
        "lowest_price": True,
        "lowest_price_without_no_change": False,
        "price_decline": True,
        "price_rise": False,
    },
}
