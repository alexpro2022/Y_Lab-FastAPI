from pydantic import SecretStr  # EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # constants
    URL_PREFIX: str = '/api/v1/'
    DEFAULT_STR: str = 'To be implemented in .env file'
    SUPER_ONLY: str = '__Только для суперюзеров:__ '
    AUTH_ONLY: str = '__Только для авторизованных пользователей:__ '
    ALL_USERS: str = '__Для всех пользователей:__ '

    # environment variables
    app_title: str = DEFAULT_STR
    app_description: str = DEFAULT_STR
    secret_key: SecretStr = DEFAULT_STR
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'  # for Alembic migrations and GitHub tests
    redis_url: str = 'redis://redis:6379'
    redis_expire: int = 3600
    rabbitmq_port: int = 5672
    celery_broker_url: str = f'amqp://guest:guest@rabbitmq:{rabbitmq_port}//'
    celery_task_period: int = 15


settings = Settings()
