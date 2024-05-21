from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os

DEFAULT_KEY = "secret_key"


class AuthConfig(BaseSettings):
    secret_key: SecretStr = DEFAULT_KEY
    db_name: str = os.path.abspath("user_management.db")

    class Config:
        env_prefix = "AUTH_"


AUTH_SETTINGS = AuthConfig()
