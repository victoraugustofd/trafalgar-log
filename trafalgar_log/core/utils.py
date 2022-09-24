import json
import logging
import os
import sys
from datetime import datetime
from logging import Logger, LogRecord, StreamHandler
from typing import Any, NoReturn, Union

from pythonjsonlogger.jsonlogger import JsonFormatter

from trafalgar_log.app import SETTINGS, DEFAULT_FIELDS_TO_SHAMBLE
from trafalgar_log.core.enums import LogFields

APP: str = LogFields.APP.value
FLOW: str = LogFields.FLOW.value
CODE_LINE: str = LogFields.CODE_LINE.value
CORRELATION_ID: str = LogFields.CORRELATION_ID.value
DATE_TIME: str = LogFields.DATE_TIME.value
DOMAIN: str = LogFields.DOMAIN.value
INSTANCE_ID: str = LogFields.INSTANCE_ID.value
LOG_CODE: str = LogFields.LOG_CODE.value
LOG_MESSAGE: str = LogFields.LOG_MESSAGE.value
PAYLOAD: str = LogFields.PAYLOAD.value
SEVERITY: str = LogFields.SEVERITY.value
TIMESTAMP: str = LogFields.TIMESTAMP.value
STACKTRACE: str = "stacktrace"
ALL_FIELDS_TO_SHAMBLE: list = DEFAULT_FIELDS_TO_SHAMBLE
ALL_FIELDS_TO_SHAMBLE.extend(SETTINGS.get("SHAMBLES").split(","))
FIELDS_TO_SHAMBLE = [field.strip().lower() for field in ALL_FIELDS_TO_SHAMBLE]
SHAMBLE_CHARACTER = "*"


class TrafalgarLogFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict,
        record: LogRecord,
        message_dict: dict,
    ) -> NoReturn:
        from trafalgar_log.core.logger import Logger

        super(TrafalgarLogFormatter, self).add_fields(
            log_record, record, message_dict
        )

        log_record[APP] = SETTINGS.get("APP_NAME")
        log_record[FLOW] = Logger.get_flow()
        log_record[CODE_LINE] = _get_code_line(record)
        log_record[CORRELATION_ID] = Logger.get_correlation_id()
        log_record[DATE_TIME] = _get_date_time(record)
        log_record[DOMAIN] = SETTINGS.get(DOMAIN)
        log_record[INSTANCE_ID] = Logger.get_instance_id()
        log_record[LOG_MESSAGE] = record.message
        log_record[TIMESTAMP] = _get_timestamp(record)

        _set_stacktrace(log_record)


def _get_os_paths() -> list:
    return [
        "".join([path, os.sep])
        for path in sorted(
            map(os.path.abspath, sys.path), key=len, reverse=True
        )
        if not path.endswith(os.sep)
    ]


def _find_relative_path(record: LogRecord) -> str:
    # ensure that the path separator is always the os separator
    pathname = record.pathname.replace("/", os.sep)
    file_name = os.path.basename(record.filename)

    return next(
        os.path.relpath(pathname, path)
        for path in OS_PATHS
        if pathname.startswith(path)
        and file_name != os.path.relpath(pathname, path)
    )


def _get_code_line(record: LogRecord) -> str:
    relativepath = _find_relative_path(record)

    return (
        f"{relativepath.replace(os.sep, '/')} - "
        f"{record.funcName}:{record.lineno}"
    )


def _get_date_time(record: LogRecord) -> str:
    return datetime.fromtimestamp(record.created, tz=None).isoformat(
        sep=" ", timespec="milliseconds"
    )


def _get_timestamp(record: LogRecord) -> int:
    return int(record.created * 1000)


def _set_stacktrace(log_record: dict) -> NoReturn:
    if log_record.get("exc_info"):
        log_record[STACKTRACE] = log_record.pop("exc_info").split("\n")


def _get_format() -> str:
    return " ".join([f"%({log_field.value})" for log_field in LogFields])


def _get_formatter() -> TrafalgarLogFormatter:
    return TrafalgarLogFormatter(_get_format())


def _remove_handlers() -> NoReturn:
    root = logging.getLogger()

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)


def _get_handler() -> StreamHandler:
    log_handler = StreamHandler()
    log_handler.setFormatter(_get_formatter())
    return log_handler


def _shamble_list(value: list) -> list:
    return [SHAMBLE_CHARACTER for _ in value]


def _is_iterable(obj) -> bool:
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def _is_primitive(obj) -> bool:
    return isinstance(obj, str) or (
        not hasattr(obj, "__dict__") and not _is_iterable(obj)
    )


def _should_shamble_primitive_value(key, value) -> bool:
    return _is_primitive(value) and key.lower() in FIELDS_TO_SHAMBLE


def _shamble_fields(payload) -> dict:
    if isinstance(payload, dict):
        return _dict_replace_value(payload)

    return payload


# refs.: https://stackoverflow.com/a/60776516/7973282
def _dict_replace_value(payload) -> dict:
    new_payload = {}

    for key, value in payload.items():
        if isinstance(value, dict):
            value = _dict_replace_value(value)
        elif isinstance(value, list):
            value = _shamble_list(value)
        elif _should_shamble_primitive_value(key, value):
            value = SHAMBLE_CHARACTER
        new_payload[key] = value
    return new_payload


def _to_json(payload: object) -> Union[str, dict]:
    return json.loads(
        json.dumps(
            payload,
            skipkeys=True,
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o),
        )
    )


def get_payload(payload: object) -> Union[object, dict]:
    return _shamble_fields(_to_json(payload))


def initialize_logger() -> Logger:
    # remove handlers to avoid conflict and log duplication
    # refs.: https://stackoverflow.com/a/45624044/7973282
    _remove_handlers()

    logger = logging.getLogger(SETTINGS.get("APP_NAME"))
    logger.addHandler(_get_handler())
    logger.setLevel(logging.getLevelName(SETTINGS.get("HAKI")))

    return logger


OS_PATHS = _get_os_paths()
