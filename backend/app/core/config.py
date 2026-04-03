from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding='utf-8')

    db_url: str = "postgresql+asyncpg://username:password@localhost:5432/acetariaa"
    cors_origins: str = "http://localhost:5173"
    api_prefix: str = "/api/v1"
    acetaria_auto_seed: int = 0

    discord_client_id: str = ""
    discord_client_secret: str = ""
    discord_redirect_uri: str = "http://localhost:8000/api/v1/auth/discord/callback"
    discord_oauth_scope: str = "identify"
    discord_admin_id: str = ""

    session_secret: str = "change-me-in-env"
    session_max_age_seconds: int = 60 * 60 * 24 * 7
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    frontend_url: str = "http://localhost:5173"
    frontend_oauth_success_redirect: str = "http://localhost:5173/"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
