import logging
from logging import INFO, DEBUG, WARN, ERROR, CRITICAL

from trafalgar_log.core.utils import (
    initialize_logger,
    LOG_CODE,
    PAYLOAD,
    SEVERITY,
    get_payload,
)

_logger = initialize_logger()


class _TrafalgarLogger(object):
    def info(self, log_code: str, log_message: str, payload: object):
        if _logger.isEnabledFor(INFO):
            self._do_log(INFO, log_code, log_message, payload)

    def debug(self, log_code: str, log_message: str, payload: object):
        if _logger.isEnabledFor(DEBUG):
            self._do_log(DEBUG, log_code, log_message, payload)

    def warn(self, log_code: str, log_message: str, payload: object):
        if _logger.isEnabledFor(WARN):
            self._do_log(WARN, log_code, log_message, payload)

    def error(self, log_code: str, log_message: str, payload: object):
        if _logger.isEnabledFor(ERROR):
            self._do_log(ERROR, log_code, log_message, payload)

    def critical(self, log_code: str, log_message: str, payload: object):
        if _logger.isEnabledFor(CRITICAL):
            self._do_log(CRITICAL, log_code, log_message, payload)

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


Logger = _TrafalgarLogger()
