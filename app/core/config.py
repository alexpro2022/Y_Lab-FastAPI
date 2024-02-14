from pydantic import SecretStr
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
    rabbitmq_port: int = 5672
    celery_broker_url: str = f'amqp://guest:guest@rabbitmq:{rabbitmq_port}//'
    celery_task_period: int = 15

    # Переменные для Google API
    google_sheets: bool
    type: str | None = None
    project_id: str | None = None
    private_key_id: str | None = None
    private_key: str | None = None
    client_email: str | None = None
    client_id: str | None = None
    auth_uri: str | None = None
    token_uri: str | None = None
    auth_provider_x509_cert_url: str | None = None
    client_x509_cert_url: str | None = None
    spreadsheet_title: str | None = None


settings = Settings()
