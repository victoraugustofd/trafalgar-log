from enum import Enum


class LogFields(Enum):
    APP = "app"
    CHANNEL = "channel"
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
