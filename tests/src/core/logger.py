LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s\t%(levelname)s\t[%(filename)s::%(funcName)s:%(lineno)s]\t%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console"]},
        "tests": {"level": "DEBUG", "handlers": ["console"]},
    },
}
