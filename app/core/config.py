from functools import lru_cache
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Multi-tenant-Event-Booking-Ticketing-Platform"
    environment: str = "development"
    debug: bool = "DEBUG"

    database_url: PostgresDsn

    access_token_expire_minutes: float = "access_token_expire_minutes"
    refresh_token_expire_days: float = "refresh_token_expire_days"
    secret_key: str = "secret_key"
    algo: str = "algo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()