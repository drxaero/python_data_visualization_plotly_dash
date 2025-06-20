from logging import Filter, LogRecord
from logging.config import dictConfig

from config import DevConfig, config


class EmailObfuscationFilter(Filter):
    """
    Obfuscate email addresses as an "extra argument to the log record". For example:
    `log.debug(msg, extra={"email": "bob@example.net"})`.
    To ensure the full email address is not logged, this filter replaces the email address with "bo*@example.net".
    """

    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    @staticmethod
    def _obfuscate(email: str, obfuscated_length: int) -> str:
        """
        Obfuscate an email address by replacing part of the local part with asterisks.

        This method replaces the email address "bob@example.net" with "bo*@example.net", where the number of visible
        characters in the local part is determined by the `obfuscated_length` parameter.

        :param email: The email address to obfuscate.
        :param obfuscated_length: The number of characters to leave unobfuscated in the local part of the email address.
        :return: The obfuscated email address.
        """
        user_plain = email[:obfuscated_length]
        user, domain = email.split("@")
        return user_plain + ("*" * (len(user) - obfuscated_length)) + "@" + domain

    def filter(self, record: LogRecord) -> bool:
        """
        Obfuscate email addresses as an "extra argument to the log record". For example:
        `log.debug(msg, extra={"email": "bob@example.net"})`.
        To ensure the full email address is not logged, the filter replaces the email address with "bo*@example.net".

        :return: `True` if the record should be processed; `False` if the record should be filtered out.
        """
        if "email" in record.__dict__:
            email = record.__dict__["email"]
            if isinstance(email, str) and "@" in email:
                record.email = self._obfuscate(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    app1_handlers = ["default", "rotating_file"]

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S.%f%z",
                    "format": "%(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    # "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    # For JsonFormatter, the format string just defines what keys are included in the log record
                    # It's a bit clunky, but it's the way to do it for now
                    # Why padding with 8? Because the maximum length of levelname is "CRITICAL" which has 8 characters
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["email_obfuscation"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "dash.log",
                    "maxBytes": 1024 * 1024,  # 1 MiB
                    "backupCount": 3,
                    "encoding": "utf8",
                    "filters": ["email_obfuscation"],
                },
            },
            "loggers": {
                "app1": {
                    "handlers": app1_handlers,
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,  # this is the top level logger, no need to propagate to the upper level
                },
            },
        }
    )
