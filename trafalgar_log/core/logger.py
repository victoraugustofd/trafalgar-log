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
    NOT_SET,
)

_logger = initialize_logger()


class Logger(object):
    """
    This is the main class of Trafalgar Log. The Logger class only has
    static methods that should be called from anywhere of an application.
    There are five log methods, each one representing a log level of the
    logging package: INFO, DEBUG, WARN, ERROR and CRITICAL.
    There are other six methods that should be used to set or retrieve the
    optional fields correlation_id, flow and instance_id.
    The _do_log function should never be called directly, that is why its
    name starts with an underscore, emulating a "private" behaviour.
    Here are the list of the available functions:

    Log functions
    :func info(log_code: str, log_message: str, payload: object) -> NoReturn
    :func debug(log_code: str, log_message: str, payload: object) -> NoReturn
    :func warn(log_code: str, log_message: str, payload: object) -> NoReturn
    :func error(log_code: str, log_message: str, payload: object) -> NoReturn
    :func critical(log_code: str, log_message: str, payload: object) ->
    NoReturn

    Optional log fields functions:
    :func set_correlation_id(correlation_id: str) -> NoReturn
    :func get_correlation_id() -> str
    :func set_flow(flow: str) -> NoReturn
    :func get_flow() -> str:
    :func set_instance_id(instance_id: str) -> NoReturn
    :func get_instance_id() -> str
    """

    correlation_id: str
    flow: str
    instance_id: str

    @staticmethod
    def info(log_code: str, log_message: str, payload: object) -> NoReturn:
        """
        The info function is a convenience function that logs a message with
        the INFO level.

        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        if _logger.isEnabledFor(INFO):
            Logger._do_log(INFO, log_code, log_message, payload)

    @staticmethod
    def debug(log_code: str, log_message: str, payload: object) -> NoReturn:
        """
        The debug function is a convenience function that logs a message with
        the DEBUG level.

        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        if _logger.isEnabledFor(DEBUG):
            Logger._do_log(DEBUG, log_code, log_message, payload)

    @staticmethod
    def warn(log_code: str, log_message: str, payload: object) -> NoReturn:
        """
        The warn function is a convenience function that logs a message with
        the WARN level.

        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        if _logger.isEnabledFor(WARN):
            Logger._do_log(WARN, log_code, log_message, payload)

    @staticmethod
    def error(log_code: str, log_message: str, payload: object) -> NoReturn:
        """
        The error function is a convenience function that logs a message with
        the ERROR level.

        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        if _logger.isEnabledFor(ERROR):
            Logger._do_log(ERROR, log_code, log_message, payload)

    @staticmethod
    def critical(log_code: str, log_message: str, payload: object) -> NoReturn:
        """
        The critical function is a convenience function that logs a message
        with the CRITICAL level.

        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        if _logger.isEnabledFor(CRITICAL):
            Logger._do_log(CRITICAL, log_code, log_message, payload)

    @staticmethod
    def set_correlation_id(correlation_id: str) -> NoReturn:
        """
        The set_correlation_id function sets the correlation_id for a log
        event.

        The correlation_id is used to track logs and metrics across services.
        It can be retrieved from the context object using get_correlation_id().
        If no correlation id has been set, it will generate a new one on each
        call.

        :param correlation_id: str: Set the correlation_id for the current
                log event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        try:
            UUID(correlation_id, version=4)
        except (ValueError, AttributeError):
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
        """
        The get_correlation_id function is a helper function that returns the
        correlation id for the current log event. If no correlation id is
        present, it will generate one and return it.

        :returns: A random uuid or the previous correlation_id setted.
        :doc-author: Trelent and this project contributors.
        """

        try:
            return Logger.correlation_id
        except AttributeError:
            correlation_id = str(uuid4())
            Logger.set_correlation_id(correlation_id)

            return correlation_id

    @staticmethod
    def set_flow(flow: str) -> NoReturn:
        """
        The set_flow function sets the global variable Logger.flow to the
        value of flow.

        :param flow: str: Set the flow for the current log event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        Logger.flow = flow

    @staticmethod
    def get_flow() -> str:
        """
        The get_flow function returns the current flow of the log event.

        :returns: The flow of the log event or the constant NOT_SET if it is
                not present.
        :doc-author: Trelent and this project contributors.
        """

        try:
            return Logger.flow
        except AttributeError:
            return NOT_SET

    @staticmethod
    def set_instance_id(instance_id: str) -> NoReturn:
        """
        The set_instance_id function sets the global variable
        Logger.instance_id to the value of instance_id.

        :param instance_id: str: Set the instance_id for the current log event.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

        Logger.instance_id = instance_id

    @staticmethod
    def get_instance_id() -> str:
        """
        The get_instance_id function returns the current instance ID of the
        log event or the constant NOT_SET if it is not present.

        :returns: The instance_id of the log event or the constant NOT_SET if
                it is not present.
        :doc-author: Trelent and this project contributors.
        """

        try:
            return Logger.instance_id
        except AttributeError:
            return NOT_SET

    @staticmethod
    def _do_log(
        level: int,
        log_code: str,
        log_message: str,
        payload: object,
    ) -> NoReturn:
        """
        The _do_log function is a helper function that is used to log messages
        to the Python logger. Its purpose is to abstract away all the
        logging details and provide a single location for managing logging
        settings.
        The function adds extra fields (log_code, payload and severity) to
        the log record.
        If the logging level is ERROR or CRITICAL, the log event uses the
        method "exception" so the logging mechanism can capture the
        exception stacktrace automatically and set the stack level to 4,
        so it can get the real caller of the log event.
        If the logging level is not ERROR or CRITICAL, the log event uses
        the method "log" and set the stack level to 3, so it can get the real
        caller of the log event.

        :param level: int: Determine the level of the log message
        :param log_code: str: A string code that identifies the type of log
                being performed. This is used to identify and filter logs in
                external applications, such as Sentry or Splunk.
        :param log_message: str: The message to be logged.
        :param payload: object: An object containing additional information
                about this specific occurrence of an event. If the payload
                is an exception, it converts it to string to avoid infinity
                recursive conversion.
        :returns: Nothing.
        :doc-author: Trelent and this project contributors.
        """

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
