from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os

DEFAULT_KEY = "secret_key"
DEFAULT_DB = os.path.abspath(os.path.join(os.getcwd(), "user_management.db"))


class AuthConfig(BaseSettings):
    secret_key: SecretStr = DEFAULT_KEY
    db_name: str = DEFAULT_DB

    class Config:
        env_prefix = "AUTH_"


AUTH_SETTINGS = AuthConfig()
