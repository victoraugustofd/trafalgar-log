import logging
from logging import INFO, DEBUG, WARN, ERROR, CRITICAL
from typing import NoReturn
from uuid import uuid4, UUID

from trafalgar_log.core.utils import (
    LOG_CODE,
    PAYLOAD,
    SEVERITY,
    initialize_logger,
    get_payload,
)

_logger = initialize_logger()


class Logger(object):
    correlation_id: str
    flow: str
    instance_id: str

    @staticmethod
    def info(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(INFO):
            Logger._do_log(INFO, log_code, log_message, payload)

    @staticmethod
    def debug(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(DEBUG):
            Logger._do_log(DEBUG, log_code, log_message, payload)

    @staticmethod
    def warn(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(WARN):
            Logger._do_log(WARN, log_code, log_message, payload)

    @staticmethod
    def error(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(ERROR):
            Logger._do_log(ERROR, log_code, log_message, payload)

    @staticmethod
    def critical(log_code: str, log_message: str, payload: object) -> NoReturn:
        if _logger.isEnabledFor(CRITICAL):
            Logger._do_log(CRITICAL, log_code, log_message, payload)

    @staticmethod
    def set_correlation_id(correlation_id: str) -> NoReturn:
        try:
            UUID(correlation_id, version=4)
        except ValueError:
            old_correlation_id = correlation_id
            correlation_id = str(uuid4())
            Logger.warn(
                log_code="Trafalgar Log",
                log_message=f"Invalid correlation_id ({old_correlation_id}). "
                f"It should be a valid uuid4.",
                payload=f"New correlation_id: {correlation_id}",
            )
        Logger.correlation_id = correlation_id

    @staticmethod
    def get_correlation_id() -> str:
        try:
            return Logger.correlation_id
        except AttributeError:
            return str(uuid4())

    @staticmethod
    def set_flow(flow: str) -> NoReturn:
        Logger.flow = flow

    @staticmethod
    def get_flow() -> str:
        try:
            return Logger.flow
        except AttributeError:
            return "NOT_SET"

    @staticmethod
    def set_instance_id(instance_id: str) -> NoReturn:
        Logger.instance_id = instance_id

    @staticmethod
    def get_instance_id() -> str:
        try:
            return Logger.instance_id
        except AttributeError:
            return "NOT_SET"

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
            _logger.exception(log_message, **extra_fields, stacklevel=4)
        else:
            _logger.log(level, log_message, **extra_fields, stacklevel=3)
