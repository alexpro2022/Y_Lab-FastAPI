from pydantic import SecretStr  # EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # constants
    URL_PREFIX: str = '/api/v1/'
    DEFAULT_STR: str = 'To be implemented in .env file'

    # environment variables
    app_title: str = DEFAULT_STR
    app_description: str = DEFAULT_STR
    secret_key: SecretStr = DEFAULT_STR
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'  # for GitHub tests


settings = Settings()
