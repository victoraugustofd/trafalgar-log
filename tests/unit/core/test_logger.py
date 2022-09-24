import json
import logging
import re
import traceback
from datetime import datetime
from logging import Logger, INFO, DEBUG, WARN, ERROR, CRITICAL
from uuid import UUID, uuid4

import pytest
from _pytest.logging import LogCaptureFixture

from trafalgar_log.core.utils import (
    initialize_logger,
    APP,
    FLOW,
    CODE_LINE,
    CORRELATION_ID,
    DATE_TIME,
    DOMAIN,
    INSTANCE_ID,
    LOG_MESSAGE,
    TIMESTAMP,
    LOG_CODE,
    PAYLOAD,
    SEVERITY,
    STACKTRACE,
)

LOG_CODE_TEST: str = "Trafalgar Log Unit Test"
CODE_LINE_PATTERN = re.compile("^(.*?)\\.py - \\w+:\\d+")
DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"
NOT_SET: str = "NOT_SET"
_logger: Logger


def setup_function():
    global _logger
    _logger = initialize_logger()


def _set_formatter(caplog: LogCaptureFixture):
    global _logger
    caplog.handler.setFormatter(_logger.handlers[0].formatter)


def _assert_code_line(log_json: dict):
    assert CODE_LINE_PATTERN.match(log_json.get(CODE_LINE))


def _assert_correlation_id(log_json: dict):
    try:
        UUID(log_json.get(CORRELATION_ID), version=4)
    except ValueError:
        pytest.fail(f"Correlation ID should be a valid uuid4.")


def _assert_datetime(log_json: dict):
    try:
        datetime.strptime(log_json.get(DATE_TIME), DATE_TIME_FORMAT)
    except ValueError:
        pytest.fail(f"Date time should be on format: yyyy-mm-dd hh:MM:ss.SSS.")


def _assert_timestamp(log_json):
    timestamp = log_json.get(TIMESTAMP)

    assert isinstance(timestamp, int)
    assert len(str(timestamp)) == 13

    try:
        datetime.fromtimestamp(timestamp / 1000)
    except Exception:
        pytest.fail("Invalid timestamp.")


def _run_asserts_exception(
    log: str, log_level: int, log_code: str, log_message: str, payload: object
):
    log_json: dict = json.loads(log)
    stacktrace: str = log_json.get(STACKTRACE)
    captured_stacktrace: str = traceback.format_exc()

    _run_asserts(log, log_level, log_code, log_message, payload)

    assert isinstance(stacktrace, list)
    assert "\n".join(stacktrace) == captured_stacktrace.strip()


def _run_asserts(
    log: str, log_level: int, log_code: str, log_message: str, payload: object
):
    try:
        log_json: dict = json.loads(log)

        assert log_json.get(APP) == "unit-tests"
        assert log_json.get(FLOW) == NOT_SET
        _assert_code_line(log_json)
        _assert_correlation_id(log_json)
        _assert_datetime(log_json)
        assert log_json.get(DOMAIN) == "tests"
        assert log_json.get(INSTANCE_ID) == NOT_SET
        assert log_json.get(LOG_CODE) == log_code
        assert log_json.get(LOG_MESSAGE) == log_message
        assert log_json.get(PAYLOAD) == payload
        assert log_json.get(SEVERITY) == logging.getLevelName(log_level)
        _assert_timestamp(log_json)
    except ValueError:
        pytest.fail("Log event should be a valid JSON")


def test_info(caplog: LogCaptureFixture):
    from trafalgar_log.core.logger import Logger

    _set_formatter(caplog)

    log_code: str = LOG_CODE_TEST
    log_message: str = "Testing info method"
    payload: object = ""

    Logger.info(log_code, log_message, payload)

    _run_asserts(caplog.text, INFO, log_code, log_message, payload)


def test_debug(caplog: LogCaptureFixture):
    from trafalgar_log.core.logger import Logger

    _set_formatter(caplog)

    log_code: str = LOG_CODE_TEST
    log_message: str = "Testing debug method"
    payload: object = ""

    Logger.debug(log_code, log_message, payload)

    _run_asserts(caplog.text, DEBUG, log_code, log_message, payload)


def test_warn(caplog: LogCaptureFixture):
    from trafalgar_log.core.logger import Logger

    _set_formatter(caplog)

    log_code: str = LOG_CODE_TEST
    log_message: str = "Testing warn method"
    payload: object = ""

    Logger.warn(log_code, log_message, payload)

    _run_asserts(caplog.text, WARN, log_code, log_message, payload)


def test_error(caplog: LogCaptureFixture):
    from trafalgar_log.core.logger import Logger

    _set_formatter(caplog)

    log_code: str = LOG_CODE_TEST
    log_message: str = "Testing error method"
    payload: object = ""
    force_exception: dict = {}

    try:
        force_exception["invalid_key"]
    except Exception:
        Logger.error(log_code, log_message, payload)

        _run_asserts_exception(
            caplog.text, ERROR, log_code, log_message, payload
        )


def test_critical(caplog: LogCaptureFixture):
    from trafalgar_log.core.logger import Logger

    _set_formatter(caplog)

    log_code: str = LOG_CODE_TEST
    log_message: str = "Testing critical method"
    payload: object = ""
    force_exception: dict = {}

    try:
        force_exception["invalid_key"]
    except Exception:
        Logger.critical(log_code, log_message, payload)

        _run_asserts_exception(
            caplog.text, CRITICAL, log_code, log_message, payload
        )


def test_set_correlation_id():
    from trafalgar_log.core.logger import Logger

    correlation_id: str = str(uuid4())

    Logger.set_correlation_id(correlation_id)

    assert Logger.correlation_id == correlation_id


def test_get_correlation_id():
    from trafalgar_log.core.logger import Logger

    correlation_id: str = str(uuid4())

    Logger.set_correlation_id(correlation_id)

    assert Logger.get_correlation_id() == correlation_id


def test_set_flow():
    from trafalgar_log.core.logger import Logger

    flow: str = "Unit testing flow"

    Logger.set_flow(flow)

    assert Logger.flow == flow


def test_get_flow():
    from trafalgar_log.core.logger import Logger

    del Logger.flow

    assert Logger.get_flow() == NOT_SET

    flow: str = "Unit testing flow"

    Logger.set_flow(flow)

    assert Logger.get_flow() == flow


def test_set_instance_id():
    from trafalgar_log.core.logger import Logger

    instance_id: str = "Unit testing instance_id"

    Logger.set_instance_id(instance_id)

    assert Logger.instance_id == instance_id


def test_get_instance_id():
    from trafalgar_log.core.logger import Logger

    del Logger.instance_id

    assert Logger.get_instance_id() == NOT_SET

    instance_id: str = "Unit testing instance_id"

    Logger.set_instance_id(instance_id)

    assert Logger.get_instance_id() == instance_id
