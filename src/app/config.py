import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Awesome API'
    admin_email: str = 'example@email.com'
    base_dir: pathlib.Path = pathlib.Path(__file__).resolve().parent
    items_per_user: int = 50
    database_url: str
    echo: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
