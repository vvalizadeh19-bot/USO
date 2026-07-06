"""Application configuration.

Settings are loaded from environment variables (and an optional ``.env`` file).
The platform targets PostgreSQL in production, but falls back to a local SQLite
file so the backend can run and be tested without a database server.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- General ---
    app_name: str = "USO Enterprise Platform"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api"

    # --- Database ---
    # Example (Postgres): postgresql+psycopg2://uso:uso@localhost:5432/uso
    database_url: str = "sqlite:///./uso.db"

    # --- Security / JWT ---
    secret_key: str = Field(
        default="CHANGE-ME-IN-PRODUCTION-use-a-long-random-string",
        description="HMAC signing key for JWT tokens.",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15   # SEC §7.5
    refresh_token_expire_minutes: int = 8 * 60

    # --- Password policy (SEC §7.4) ---
    password_min_length: int = 12

    # --- CPM import (§2.3–2.4) ---
    # Header row is auto-detected by default; set to force a specific row.
    cpm_header_row: int | None = None

    # --- Bootstrap admin (created by seed script if absent) ---
    admin_username: str = "admin"
    admin_password: str = "ChangeMe!Admin1"
    admin_email: str = "admin@uso.example.com"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
