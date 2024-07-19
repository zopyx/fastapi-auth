from pydantic_settings import BaseSettings
from pydantic import SecretStr

DEFAULT_KEY = SecretStr("secret_key")
DEFAULT_DB_URI = "sqlite:///user_management.db"


class AuthConfig(BaseSettings):
    secret_key: SecretStr = DEFAULT_KEY
    db_uri: str = DEFAULT_DB_URI
    log_filename: str = "fastpi_auth.log"
    always_superuser: bool = False

    model_config = ConfigDict(
        env_prefix="AUTH_",
    )


AUTH_SETTINGS = AuthConfig()
