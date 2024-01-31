from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    db_host: str = 'db'
    db_port: str = '5432'
    postgres_db: str = 'postgres'

    @property
    def database_url(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.postgres_user}:{self.postgres_password}@'
                f'{self.db_host}:{self.db_port}/{self.postgres_db}')


settings = Settings()
