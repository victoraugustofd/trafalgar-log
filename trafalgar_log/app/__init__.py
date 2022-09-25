"""
This is the Dynaconf configuration.

Trafalgar Log accept four environment variables:
- TRA_LOG_APP_NAME (mandatory): This is the environment variable that
  will be used as the "app" field in the log event.
- TRA_LOG_DOMAIN (mandatory): This is the environment variable that
  will be used as the "domain" field in the log event.
- TRA_LOG_HAKI (mandatory): This is the environment variable that
  will be used to set the logging level for the application.
- TRA_LOG_SHAMBLES (mandatory): This is the environment variable with the
  fields that should be shambled on the log event.
"""

import logging
from logging import INFO, DEBUG, WARN, ERROR, CRITICAL

from dynaconf import Dynaconf, Validator, ValidationError

HAKI_LEVELS = [
    logging.getLevelName(level)
    for level in [INFO, DEBUG, WARN, ERROR, CRITICAL]
]
DEFAULT_FIELDS_TO_SHAMBLE: list = ["password", "senha", "contraseña"]
SETTINGS = Dynaconf(
    envvar_prefix="TRA_LOG",
    load_dotenv=True,
    validators=[
        Validator(
            "APP_NAME",
            "DOMAIN",
            must_exist=True,
        ),
        Validator(
            "HAKI",
            default="INFO",
            condition=lambda x: x.upper() in HAKI_LEVELS,
        ),
        Validator("SHAMBLES", default=""),
    ],
)

try:
    SETTINGS.validators.validate_all()
except ValidationError as e:
    print(f"Exception initializing Trafalgar Log: {str(e)}")
