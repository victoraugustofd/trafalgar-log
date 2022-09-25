from enum import Enum


class LogFields(Enum):
    """
    This is an enum class used to list all fields from a log event.

    :cvar APP: Represents the application name that generated the log event.
    :cvar FLOW: This field should be used as an identifier of who estimulated
        the application to start the execution which is being logged.
    :cvar CODE_LINE: Code line that the log event occurred; it will be printed
        as path/to/file.py - function_name:code_line.
    :cvar CORRELATION_ID: ID used to trace a single execution, end-to-end;
        this is an uuid4.
    :cvar DATE_TIME: Datetime of the log event on the format
        yyyy-MM-dd hh:mm:ss.SSS - e.g., 2022-09-18 19:25:43.749
    :cvar DOMAIN: Application domain that can be used to represent the
        functional domain of the application.
    :cvar INSTANCE_ID: ID used to represent the application instance; it can
        be an IP Address, an ID of a lambda funcion instance, etc.
    :cvar LOG_CODE: A String that represents a general purpose of the log
        event; it can be used to represent all logs of database operations, for
        example.
    :cvar LOG_MESSAGE: The log message that you want to print.
    :cvar PAYLOAD: This can be literally anything; if it is a primitive type,
        it will be printed as it is, but if it is a complex object, a list or
        even a dict, it will be printed as a JSON object.
    :cvar SEVERITY: The log level of the log event.
    :cvar TIMESTAMP: Timestamp of the log event in milliseconds.
    """

    APP = "app"
    FLOW = "flow"
    CODE_LINE = "code_line"
    CORRELATION_ID = "correlation_id"
    DATE_TIME = "date_time"
    DOMAIN = "domain"
    INSTANCE_ID = "instance_id"
    LOG_CODE = "log_code"
    LOG_MESSAGE = "log_message"
    PAYLOAD = "payload"
    SEVERITY = "severity"
    TIMESTAMP = "timestamp"
