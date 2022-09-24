from dynaconf import Dynaconf, Validator, ValidationError

from trafalgar_log.core.exceptions import ConfigurationError

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
        Validator("HAKI", default="INFO"),
        Validator("SHAMBLES", default=""),
    ],
)

try:
    SETTINGS.validators.validate_all()
except ValidationError as e:
    raise ConfigurationError()
