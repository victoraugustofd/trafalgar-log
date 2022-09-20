from dynaconf import Dynaconf, Validator, ValidationError

from trafalgar_log.core.exceptions import ConfigurationError

SETTINGS = Dynaconf(
    envvar_prefix="TRA_LOG",
    load_dotenv=True,
    validators=[
        Validator(
            "APP_NAME",
            "DOMAIN",
            must_exist=True,
        ),
        Validator("LOG_LEVEL", default="INFO"),
        Validator("FIELDS_TO_MASK", default=[]),
    ],
)

try:
    SETTINGS.validators.validate_all()
except ValidationError as e:
    raise ConfigurationError()
