from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DB_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/postgres'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    database_url: str = DEFAULT_DB_URL


settings = Settings()
