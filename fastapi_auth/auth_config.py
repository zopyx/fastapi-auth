from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os

DEFAULT_KEY = "secret_key"
DEFAULT_DB_URI = "sqlite:///user_management.db"


class AuthConfig(BaseSettings):
    secret_key: SecretStr = DEFAULT_KEY
    db_uri: str = DEFAULT_DB_URI

    class Config:
        env_prefix = "AUTH_"


AUTH_SETTINGS = AuthConfig()
