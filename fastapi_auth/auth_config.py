from pydantic_settings import BaseSettings
from pydantic import SecretStr

DEFAULT_KEY = "secret_key"


class AuthConfig(BaseSettings):
    secret_key: SecretStr = DEFAULT_KEY

    class Config:
        env_prefix = "AUTH_"


AUTH_SETTINGS = AuthConfig()
