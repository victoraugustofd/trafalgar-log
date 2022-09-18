import inspect
import json
import logging
import os
import sys
from datetime import datetime
from inspect import FrameInfo
from logging import Logger, LogRecord, StreamHandler
from typing import Dict, Any, List
from uuid import uuid4

from pythonjsonlogger.jsonlogger import JsonFormatter

from trafalgar_log.app import SETTINGS
from trafalgar_log.core.enums import LogFields

APP = LogFields.APP.value
CHANNEL = LogFields.CHANNEL.value
CODE_LINE = LogFields.CODE_LINE.value
CORRELATION_ID = LogFields.CORRELATION_ID.value
DATE_TIME = LogFields.DATE_TIME.value
DOMAIN = LogFields.DOMAIN.value
INSTANCE_ID = LogFields.INSTANCE_ID.value
LOG_CODE = LogFields.LOG_CODE.value
LOG_MESSAGE = LogFields.LOG_MESSAGE.value
PAYLOAD = LogFields.PAYLOAD.value
SEVERITY = LogFields.SEVERITY.value
TIMESTAMP = LogFields.TIMESTAMP.value


class CustomJsonFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: LogRecord,
        message_dict: Dict[str, Any],
    ):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )

        log_record[APP] = SETTINGS.get("APP_NAME")
        log_record[CHANNEL] = os.getenv(CHANNEL, "NOT_SET")
        log_record[CODE_LINE] = _get_code_line()
        log_record[DATE_TIME] = _get_date_time(record)
        log_record[DOMAIN] = SETTINGS.get(DOMAIN)
        log_record[INSTANCE_ID] = os.getenv(INSTANCE_ID, "NOT_SET")
        log_record[LOG_MESSAGE] = record.message
        log_record[TIMESTAMP] = _get_timestamp(record)

        _set_correlation_id(log_record)
        _set_stacktrace(log_record)


def _get_os_paths():
    return [
        "".join([path, os.sep])
        for path in sorted(
            map(os.path.abspath, sys.path), key=len, reverse=True
        )
        if not path.endswith(os.sep)
    ]


def _find_relative_path(a, pathname):
    return next(
        os.path.relpath(pathname, path)
        for path in a
        if pathname.startswith(path)
    )


def _get_code_line():
    stack = _find_log_caller_stack()

    # ensure that the path separator is always the os separator
    pathname = stack.filename.replace("/", os.sep)
    relativepath = _find_relative_path(_get_os_paths(), pathname)

    return (
        f"{relativepath.replace(os.sep, '/')} - "
        f"{stack.function}:{stack.lineno}"
    )


def _find_log_caller_stack():
    stacks: List[FrameInfo] = inspect.stack()
    log_stack_index = [
        index
        for index, stack in enumerate(stacks)
        if stack.function == "_do_log"
    ][0]

    # since the caller method is always _do_log and it is called from
    # one of the _logger methods, the real caller is always two (2) stacks
    # before _do_log stack
    return stacks[log_stack_index + 2]


def _get_date_time(record: LogRecord):
    return datetime.fromtimestamp(record.created, tz=None).isoformat(
        sep=" ", timespec="milliseconds"
    )


def _get_timestamp(record: LogRecord):
    return int(record.created * 1000)


def _set_correlation_id(log_record: Dict[str, Any]):
    correlation_id: str = os.getenv(CORRELATION_ID)

    if not correlation_id:
        correlation_id = str(uuid4())
        os.environ[CORRELATION_ID] = correlation_id

    log_record[CORRELATION_ID] = correlation_id


def _set_stacktrace(log_record: Dict[str, Any]):
    if log_record.get("exc_info"):
        log_record["stacktrace"] = log_record.pop("exc_info").split("\n")


def _get_format():
    return " ".join([f"%({log_field.value})" for log_field in LogFields])


def _get_formatter() -> CustomJsonFormatter:
    return CustomJsonFormatter(_get_format())


def _remove_handlers():
    root = logging.getLogger()

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)


def _get_handler():
    log_handler = StreamHandler()
    log_handler.setFormatter(_get_formatter())
    return log_handler


def initialize_logger() -> Logger:
    # remove handlers to avoid conflict and log duplication
    # refs.: https://stackoverflow.com/a/45624044/7973282
    _remove_handlers()

    logger = logging.getLogger(SETTINGS.get("APP_NAME"))
    logger.addHandler(_get_handler())
    logger.setLevel(logging.getLevelName(SETTINGS.get("LOG_LEVEL")))

    return logger


def get_payload(payload: object) -> dict:
    return json.loads(
        json.dumps(
            payload,
            skipkeys=True,
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o),
        )
    )
