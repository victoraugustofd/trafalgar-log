import logging
import os
from logging import INFO, DEBUG, WARN, ERROR, CRITICAL
from typing import NoReturn

from trafalgar_log.core.utils import (
    LOG_CODE,
    PAYLOAD,
    SEVERITY,
    CORRELATION_ID,
    FLOW,
    INSTANCE_ID,
    initialize_logger,
    get_payload,
)

_logger = initialize_logger()


class Logger(object):
    
    @staticmethod
    def info(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(INFO):
            Logger._do_log(INFO, log_code, log_message, payload)

    @staticmethod
    def debug(log_code: str, log_message: str, payload:  object) -> NoReturn:
        if _logger.isEnabledFor(DEBUG):
            Logger._do_log(DEBUG, log_code, log_message, payload)

    @staticmethod
    def warn(log_code: str, log_message: str, payload:  object) -> NoReturn:
        if _logger.isEnabledFor(WARN):
            Logger._do_log(WARN, log_code, log_message, payload)

    @staticmethod
    def error(log_code: str, log_message: str, payload:  object) -> NoReturn:
        if _logger.isEnabledFor(ERROR):
            Logger._do_log(ERROR, log_code, log_message, payload)

    @staticmethod
    def critical(log_code: str, log_message: str, payload:  object) -> NoReturn:
        if _logger.isEnabledFor(CRITICAL):
            Logger._do_log(CRITICAL, log_code, log_message, payload)

    @staticmethod
    def set_correlation_id(correlation_id: str) -> NoReturn:
        os.environ[CORRELATION_ID] = correlation_id

    @staticmethod
    def set_flow(flow: str) -> NoReturn:
        os.environ[FLOW] = flow

    @staticmethod
    def set_instance_id(instance_id: str) -> NoReturn:
        os.environ[INSTANCE_ID] = instance_id

    @staticmethod
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
            _logger.exception(log_message, **extra_fields)
        else:
            _logger.log(level, log_message, **extra_fields)
