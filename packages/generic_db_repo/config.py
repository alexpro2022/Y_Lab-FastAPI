from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DB_URL = 'sqlite+aiosqlite:///./fastapi.db'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    database_url: str = DEFAULT_DB_URL


settings = Settings()
