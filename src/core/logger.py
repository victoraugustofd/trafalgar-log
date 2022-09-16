import logging
from logging import INFO, DEBUG, WARN, ERROR, CRITICAL

from src.core.utils import get_logger, LOG_CODE, PAYLOAD, SEVERITY, get_payload

logger = get_logger()


def info(log_code: str, log_message: str, payload: object):
    if logger.isEnabledFor(INFO):
        _do_log(INFO, log_code, log_message, payload)


def debug(log_code: str, log_message: str, payload: object):
    if logger.isEnabledFor(DEBUG):
        _do_log(DEBUG, log_code, log_message, payload)


def warn(log_code: str, log_message: str, payload: object):
    if logger.isEnabledFor(WARN):
        _do_log(WARN, log_code, log_message, payload)


def error(log_code: str, log_message: str, payload: object):
    if logger.isEnabledFor(ERROR):
        _do_log(ERROR, log_code, log_message, payload)


def critical(log_code: str, log_message: str, payload: object):
    if logger.isEnabledFor(CRITICAL):
        _do_log(CRITICAL, log_code, log_message, payload)


def _do_log(
    level: int,
    log_code: str,
    log_message: str,
    payload: object,
):
    if isinstance(payload, BaseException):
        payload = str(payload)

    extra_fields = {
        "extra": {
            LOG_CODE: log_code,
            PAYLOAD: get_payload(payload),
            SEVERITY: logging.getLevelName(level),
        }
    }

    if level in [ERROR, CRITICAL]:
        logger.exception(log_message, **extra_fields)
    else:
        logger.log(level, log_message, **extra_fields)
