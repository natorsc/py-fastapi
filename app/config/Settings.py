from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / 'static'


class Settings(BaseSettings):
    app: str = 'App Name'
    admin_email: str = 'admin@email.com'
    items_per_user: int = 50
    version: str = 'v1'
    static_dir: Path = STATIC_DIR
    model_config = SettingsConfigDict(env_file='.env', extra='allow')


@lru_cache
def get_settings():
    return Settings()
