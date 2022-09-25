import json
import logging
import os
import sys
from datetime import datetime
from logging import Logger, LogRecord, StreamHandler
from typing import NoReturn, Union

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
FIELDS_TO_SHAMBLE: list = [
    field.strip().lower() for field in ALL_FIELDS_TO_SHAMBLE
]
SHAMBLE_CHARACTER: str = "*"
NOT_SET: str = "NOT_SET"


class TrafalgarLogFormatter(JsonFormatter):
    """
    This is the class responsible for formatting the log record of the log
    event to the format of Trafalgar Log.
    This class is instantiated only one time at the boot of an application
    through the initialize_logger function.
    Its only function add_fields or any other functions that may be
    implemented on this class should never be called, since this is a class
    used automatically by the logging package.

    """

    def add_fields(
        self,
        log_record: dict,
        record: LogRecord,
        message_dict: dict,
    ) -> NoReturn:
        """
        The add_fields is the function responsible for the formatting
        process. This method should not be called in any circumstances,
        because it is called automatically each time a log event is created.

        :param log_record: dict: A dict containing information regarding the
                log event provided by the Logger._do_log function, such as
                log_code, payload and severity.
        :param record: LogRecord: The log record of the log event containing
                all automatically filled information provided by the logging
                package.
        :param message_dict: dict: A dict containing data that is not on the
                other two parameters.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

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
    """
    The _get_os_paths function returns a list of all the paths in sys.path
    that are not absolute (i.e., don't end with a slash). The returned list
    is sorted from longest to shortest path, to ensure that longer paths
    take precedence over shorter ones. For example,
    /opt/python_virtualenv/lib/python3.6/site-packages takes precedence over
    /opt/python_virtualenv/. Since _get_os_paths returns a copy of sys.path,
    this function can be called safely by other modules.

    :returns: A list of the OS paths.
    :doc-author: Trelent and this project contributors.
    """

    return [
        "".join([path, os.sep])
        for path in sorted(
            map(os.path.abspath, sys.path), key=len, reverse=True
        )
        if not path.endswith(os.sep)
    ]


def _find_relative_path(record: LogRecord) -> str:
    """
    The _find_relative_path function is used to find the relative path of a
    log event.

    The function is called by the _get_code_line function and takes in a
    record from the logging module. The record contains information about
    where the log was created, including what file it was created in and what
    line number it was on. The pathname attribute stores an absolute path to
    where this log message was created, while filename stores just its
    basename.

    :param record: LogRecord: The log record of the log event.
    :returns: The relative path of the log file from the os_paths.
    :doc-author: Trelent and this project contributors.
    """

    # ensure that the path separator is always the os separator
    pathname = record.pathname.replace("/", os.sep)
    file_name = os.path.basename(record.filename)

    try:
        return next(
            os.path.relpath(pathname, path)
            for path in OS_PATHS
            if pathname.startswith(path)
            and file_name != os.path.relpath(pathname, path)
        )
    except StopIteration:
        return record.filename


def _get_code_line(record: LogRecord) -> str:
    """
    The _get_code_line function is used by the
    TrafalgarLogFormatter.add_fields function to get the code
    line that a log record was created on. It does this by finding all of the
    directories in between where this file (logging/__init__.py) is located
    and where the module containing `record` (the LogRecord object) is
    located, then joining them together with slashes (/).
    The result will be something like: mypackage/module.py - myfunc:10

    :param record: LogRecord: The log record of the log event.
    :returns: A string that contains the relative path to the file where the
            log record was created, followed by a dash and then it returns a
            string containing the function name and line number of code where
            the log record was created.
    :doc-author: Trelent and this project contributors.
    """

    relativepath = _find_relative_path(record)

    return (
        f"{relativepath.replace(os.sep, '/')} - "
        f"{record.funcName}:{record.lineno}"
    )


def _get_date_time(record: LogRecord) -> str:
    """
    The _get_date_time function returns a string representation of the log
    event date and time.

    :param record: LogRecord: The log record of the log event.
    :returns: A string of the date and time in ISO 8601 format
            (yyyy-MM-dd hh:mm:ss.SSS).
    :doc-author: Trelent and this project contributors.
    """

    return datetime.fromtimestamp(record.created, tz=None).isoformat(
        sep=" ", timespec="milliseconds"
    )


def _get_timestamp(record: LogRecord) -> int:
    """
    The _get_timestamp function is a helper function that returns the
    timestamp of a log record in milliseconds.

    :param record: LogRecord: The log record of the log event.
    :returns: The time in milliseconds when the log record was created.
    :doc-author: Trelent and this project contributors.
    """

    return int(record.created * 1000)


def _set_stacktrace(log_record: dict) -> NoReturn:
    """
    The _set_stacktrace function is a helper function that is called by the
    logging.Formatter class to set the stacktrace field of each log record.

    :param log_record: dict: Set the stacktrace key in the log_record:dict
    parameter if the log record has "exc_info" key.
    :returns: Nothing.
    :doc-author: Trelent and this project contributors.
    """

    if log_record.get("exc_info"):
        log_record[STACKTRACE] = log_record.pop("exc_info").split("\n")


def _get_format() -> str:
    """
    The _get_format function returns a string that can be used to format the
    log fields for output. The returned string is a concatenation of all the
    log field names, each preceded by % and enclosed in parentheses. This
    allows us to use Python's built-in logging module's formatting
    functionality.

    :returns: A string that is used as the format for a logging.
    :doc-author: Trelent and this project contributors.
    """

    return " ".join([f"%({log_field.value})" for log_field in LogFields])


def _get_formatter() -> TrafalgarLogFormatter:
    """
    The _get_formatter function returns an instance of the
    TrafalgarLogFormatter class, which is then passed to the logging
    module's basicConfig function as the formatter keyword argument. This
    allows us to configure how our log messages are formatted before they are
    written out by setting attributes on this object.

    :returns: A TrafalgarLogFormatter object.
    :doc-author: Trelent and this project contributors.
    """

    return TrafalgarLogFormatter(_get_format())


def _remove_handlers() -> NoReturn:
    """
    The _remove_handlers function removes all handlers from the root logger.

    :returns: Nothing.
    :doc-author: Trelent and this project contributors.
    """

    root = logging.getLogger()

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)


def _get_handler() -> StreamHandler:
    """
    The _get_handler function creates a StreamHandler object and sets the
    formatter to the _get_formatter function.
    It then returns this handler.

    :returns: A StreamHandler object.
    :doc-author: Trelent and this project contributors.
    """

    log_handler = StreamHandler()
    log_handler.setFormatter(_get_formatter())
    return log_handler


def _shamble_list(value: list) -> list:
    """
    The _shamble_list function takes a list and returns a new list with the
    same elements, but with each element replaced by SHAMBLE_CHARACTER. This
    is used to hide potentially sensitive information in the log event.

    :param value: list: Tell the function the list to shamble its values.
    :returns: The list of the parameter with its contents shambled.
    :doc-author: Trelent and this project contributors.
    """

    return [SHAMBLE_CHARACTER for _ in value]


# noinspection PyTypeChecker
def _is_iterable(obj: object) -> bool:
    """
    The _is_iterable function is a helper function that is used to determine
    if an object is iterable.
    It does this by attempting to use the built-in Python iter() function on
    the object. If it succeeds, then _is_iterable returns True; otherwise it
    returns False.

    :param obj: object: The object to be tested if it is iterable.
    :returns: True if the object is iterable, False otherwise.
    :doc-author: Trelent and this project contributors.
    """

    try:
        iter(obj)
        return True
    except TypeError:
        return False


def _is_primitive(obj: object) -> bool:
    """
    The _is_primitive function is a helper function for the
    _should_shamble_primitive_value function.
    It returns True if obj is a primitive type (str, int, float), and False o
    therwise.

    :param obj: object: The object that should be checked if it is primitive.
    :returns: True if the object is a primitive (str, int, float or bool).
    :doc-author: Trelent and this project contributors.
    """

    return isinstance(obj, str) or (
        not hasattr(obj, "__dict__") and not _is_iterable(obj)
    )


def _should_shamble_primitive_value(key: str, value: object) -> bool:
    """
    The _should_shamble_primitive_value function is used to determine whether
    a primitive value should be shambled. Primitive values are those that are
    not complex objects, such as lists or dictionaries.
    The _should_shamble_primitive_value function returns True if the key of
    the given value is in the list of keys to shambler, and False otherwise.

    :param key: str: The key of the value to check if it should be shambled.
    :param value: object: The value that should be validate if it is primitive.
    :returns: True if the value is a primitive and it's key is in
            FIELDS_TO_SHAMBLE.
    :doc-author: Trelent and this project contributors.
    """

    return key.lower() in FIELDS_TO_SHAMBLE and _is_primitive(value)


def _shamble_fields(payload: object) -> Union[dict, object]:
    """
    The _shamble_fields function is a helper function that is used to replace
    the values of the fields in the payload with random values. This is done
    by using a dictionary comprehension to iterate through each key and
    value pair in the payload. The result of this function will be passed
    into _dict_replace_value which will recursively call itself on any nested
    dictionaries or lists.

    :param payload: object: The payload to be have its field replaced with a
            new value.
    :returns: A dictionary with the same keys and values as the payload
            argument, except that all of the values have been replaced by a new
            value or the payload itself if it is not a dictionary.
    :doc-author: Trelent and this project contributors.
    """

    if isinstance(payload, dict):
        return _dict_replace_value(payload)

    return payload


def _dict_replace_value(payload: dict) -> dict:
    """
    # refs.: https://stackoverflow.com/a/60776516/7973282
    The _dict_replace_value function replaces all values in a dictionary with
    the SHAMBLE_CHARACTER character. This is done to prevent sensitive
    information from being exposed in the log event.

    :param payload: dict: The payload to be have its field replaced with a
            new value.
    :returns: A new dictionary with all values that are dictionaries replaced
            by a shambled version of the value.
    :doc-author: Trelent and this project contributors.
    """

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


def _to_json(payload: object) -> dict:
    """
    The _to_json function is a helper function that converts an object to JSON.
    The _to_json function will convert all attributes within an object to
    key-value pairs and return a dict.
    If there are any nested objects, they will also be converted to dicts and
    so on.
    The skipkeys attribute is set to True so that if there are any
    unserializable attributes (which would happen if using default=lambda),
    they can be skipped instead of causing an infity loop.

    :param payload: object: The payload to be converted to JSON object.
    :returns: The JSON object.
    :doc-author: Trelent and this project contributors.
    """

    return json.loads(
        json.dumps(
            payload,
            skipkeys=True,
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o),
        )
    )


def get_payload(payload: object) -> Union[object, dict]:
    """
    The get_payload function is a helper function that takes in an object and
    returns a dictionary. The get_payload function is used to convert the
    payload from a Python object into a JSON-serializable dictionary. This
    allows the user to pass in any arbitrary Python object as the payload.

    :param payload: object: Pass in the object that is to be converted into
            a JSON object.
    :returns: A JSON serialized version of the payload or payload itself if
            it is a primitive type.
    :doc-author: Trelent and this project contributors.
    """

    return _shamble_fields(_to_json(payload))


def initialize_logger() -> Logger:
    """
    The initialize_logger function creates a logger object that is used to
    log messages.
    It also adds a handler to the logger object, which allows for logging of
    messages.
    It remove handlers to avoid conflict and log duplication.
    refs.: https://stackoverflow.com/a/45624044/7973282

    :returns: A logger object.
    :doc-author: Trelent and this project contributors.
    """

    _remove_handlers()

    logger = logging.getLogger(SETTINGS.get("APP_NAME"))
    logger.addHandler(_get_handler())
    logger.setLevel(logging.getLevelName(SETTINGS.get("HAKI").upper()))

    return logger


OS_PATHS = _get_os_paths()
